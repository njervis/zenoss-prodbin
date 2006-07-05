import os
import re
import socket
import time
import Globals

from ZODB.POSException import POSError
from _mysql_exceptions import OperationalError, ProgrammingError 

from Products.ZenUtils.ZCmdBase import ZCmdBase
from ZenEventClasses import AppStart, AppStop, HeartbeatStatus
import Event


class ZenActions(ZCmdBase):
    """
    Take actions based on events in the event manager.
    Start off by sending emails and pages.
    """


    addstate = "insert into alert_state values ('%s', '%s', '%s')"

    clearstate = """delete from alert_state where evid='%s' 
                    and userid='%s' and rule='%s'"""

#FIXME attempt to convert subquery to left join that doesn't work 
#    newsel = """select %s, evid from status s left join alert_state a
#                on s.evid=a.evid where a.evid is null and  
#                a.userid='%s' and a.rule='%s'""" 

    newsel = """select %s, evid from status where %s and evid not in 
             (select evid from alert_state where userid='%s' and rule='%s')""" 
            
    clearsel = """select %s, h.evid from history h, alert_state a 
                  where h.evid=a.evid and a.userid='%s' and a.rule='%s'"""


    def __init__(self):
        ZCmdBase.__init__(self)
        self.actions = []
        self.loadActionRules()
        if not self.options.fromaddr:
            self.options.fromaddr = "zenoss@%s" % socket.getfqdn()
        self.sendEvent(Event.Event(device=socket.getfqdn(), 
                        eventClass=AppStart, 
                        summary="zenactions started",
                        severity=0, component="zenactions"))
        

    def loadActionRules(self):
        """Load the ActionRules into the system.
        """
        self.actions = []
        for us in self.dmd.ZenUsers.getAllUserSettings():
            userid = us.getId()
            self.log.debug("loading aciton rules for:%s", userid)
            for ar in us.objectValues(spec="ActionRule"):
                if not ar.enabled: continue
                self.actions.append(ar)
                self.log.debug("action:%s for:%s loaded", ar.getId(), userid)
                

    def processRules(self, db, zem):
        """Run through all rules matching them against events.
        """
        curs = db.cursor()
        for ar in self.actions:
            cursql = ""
            try:
                fields = ar.getEventFields()
                userid = ar.getUserid()
                addr = ar.getAddress()
                data = {}
                data = data.fromkeys(fields,"")
                # get new events
                nwhere = ar.where
                if ar.delay > 0:
                    nwhere += """ and firstTime + %s < UNIX_TIMESTAMP()"""%(
                                ar.delay)
                newsel = self.newsel % (",".join(fields), nwhere,
                                        userid, ar.getId())
                self.log.debug(newsel)
                cursql = newsel
                curs.execute(newsel)
                for result in curs.fetchall():
                    evid = result[-1]
                    result = map(zem.convert, fields, result[:-1])
                    for k, v in zip(fields, result): data[k]=v
                    msg = ar.format % data
                    actfunc = getattr(self, "send"+ar.action.title())
                    actfunc(msg, addr)
                    addcmd = self.addstate%(evid, userid, ar.getId())
                    self.log.debug(addcmd)
                    cursql = addcmd
                    curs.execute(addcmd)
                     
                # get clear events
                clearsel = self.clearsel % (",".join(fields),userid,ar.getId())
                self.log.debug(clearsel)
                cursql = clearsel
                curs.execute(clearsel)
                format = "CLEAR: " + ar.format
                for result in curs.fetchall():
                    evid = result[-1]
                    result = map(zem.convert, fields, result[:-1])
                    for k, v in zip(fields, result): data[k]=v
                    msg = format % data
                    actfunc = getattr(self, "send"+ar.action.title())
                    actfunc(msg, addr)
                    delcmd = self.clearstate%(evid, userid, ar.getId())
                    self.log.debug(delcmd)
                    cursql = delcmd
                    curs.execute(delcmd)
            except (SystemExit, KeyboardInterrupt, OperationalError, POSError): 
                raise
            except:
                if cursql: self.log.warn(cursql)
                self.log.exception("action:%s",ar.getId())


    def maintenance(self, db, zem):
        """Run stored procedures that maintain the events database.
        """
        curs = db.cursor()
        for proc in zem.maintenanceProcedures:
            try:
                curs.execute("call %s();" % proc)
            except ProgrammingError:
                self.log.exception("problem with proc: '%s'", proc)


    def heartbeatEvents(self, db, zem):
        """Create events for failed heartbeats.
        """
        # build cache of existing heartbeat issues
        heartbeatState = {}
        curs = db.cursor()
        curs.execute("select device, component from status where "
                     "eventClass = '%s'" % HeartbeatStatus)
        for device, comp in curs.fetchall():
            heartbeatState[device, comp] = 1 
           
        # find current heartbeat failures
        for device, comp, secs in zem.getHeartbeat(failures=True, db=db):
            self.sendEvent(
                Event.Event(device=device, component=comp,
                    eventClass=HeartbeatStatus, 
                    summary="%s %s heartbeat failure" % (device,comp),
                    severity=Event.Error))
            if heartbeatState.has_key((device, comp)):
                del heartbeatState[device, comp]

        # clear heartbeats
        for (device, comp), val in heartbeatState.items():
            self.sendEvent(Event.Event(device=device, component=comp, 
                eventClass=HeartbeatStatus, 
                summary="%s %s heartbeat clear" % (device, comp),
                severity=Event.Clear))
                
            

    def mainbody(self):
        """main loop to run actions.
        """
        self.loadActionRules()
        zem = self.dmd.ZenEventManager
        db = zem.connect()
        self.processRules(db, zem)
        self.maintenance(db, zem)
        self.heartbeatEvents(db, zem)
        db.close()
        
    
    def run(self):
        if not self.options.cycle: 
            return self.mainbody()
        while 1:
            try:
                start = time.time()
                self.syncdb()
                self.mainbody()
                self.log.info("processed %s rules in %.2f secs", 
                               len(self.actions), time.time()-start)
                self.sendHeartbeat()
            except (SystemExit, KeyboardInterrupt): raise
            except:
                self.log.exception("unexpected exception")
            time.sleep(self.options.cycletime)


    def sendEvent(self, evt):
        """Send event to the system.
        """
        self.dmd.ZenEventManager.sendEvent(evt)


    def sendHeartbeat(self):
        """Send a heartbeat event for this monitor.
        """
        timeout = self.options.cycletime*3
        evt = Event.EventHeartbeat(socket.getfqdn(), "zenactions", timeout)
        self.sendEvent(evt)


    def stop(self):
        self.running = False
        self.log.info("stopping")
        self.sendEvent(Event.Event(device=socket.getfqdn(), 
                        eventClass=AppStop, 
                        summary="zenactions stopped",
                        severity=3, component="zenactions"))


    def sendPage(self, msg, addr):
        """Send and event to a pager.
        """
        import Pager
        rcpt = Pager.Recipient(addr)
        pmsg = Pager.Message(msg)
        #pmsg.callerid = "zenoss"
        page = Pager.Pager((rcpt,), pmsg, self.options.snpphost, 
                                         self.options.snppport)
        page.send()
        self.log.info("sent page:%s to:%s", msg, addr)
        

    def sendEmail(self, msg, addr):
        """Send an event to an email address.
        """
        import smtplib
        from email.MIMEText import MIMEText
        emsg = MIMEText(msg)
        emsg['Subject'] = "[zenoss] %s" % msg[:128]
        emsg['From'] = self.options.fromaddr
        emsg['To'] = addr
        server = smtplib.SMTP(self.options.smtphost, self.options.smtpport)
        server.sendmail(self.options.fromaddr, (addr,), emsg.as_string())
        server.quit()
        self.log.info("sent email:%s to:%s", msg, addr)


    def buildOptions(self):
        ZCmdBase.buildOptions(self)
        self.parser.add_option('--cycletime',
            dest='cycletime', default=60, type="int",
            help="check events every cycletime seconds")
        self.parser.add_option('--fromaddr',
            dest='fromaddr', default="",
            help="address from which email is sent")
        self.parser.add_option('--snpphost',
            dest='snpphost', default="localhost",
            help="snpp server to used when sending pages")
        self.parser.add_option('--snppport',
            dest='snppport', default=444, type="int",
            help="snpp port used when sending pages")
        self.parser.add_option('--smtphost',
            dest='smtphost', default="localhost",
            help="smtp server to used when sending pages")
        self.parser.add_option('--smtpport',
            dest='smtpport', default=25, type="int",
            help="smtp port used when sending pages")

if __name__ == "__main__":
    za = ZenActions()
    za.run()
