###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__="""Monitor

Base class for all Monitor or Monitor Configuration Classes.  This is
an abstract class that is used for the devices to monitors
relationship which says which monitors monitor which devices.

$Id: Monitor.py,v 1.5 2004/04/14 22:11:48 edahl Exp $"""

__version__ = "$Revision: 1.5 $"[11:-2]

from Globals import InitializeClass

from ZenModelRM import ZenModelRM
from DeviceManagerBase import DeviceManagerBase
from RRDView import RRDView
from Products.ZenWidgets import messaging

class Monitor(ZenModelRM, DeviceManagerBase, RRDView):
    meta_type = 'Monitor'

    def snmpIgnore(self):
        return True

    def breadCrumbs(self, target='dmd'):
        from Products.ZenUtils.Utils import unused
        unused(target)
        bc = ZenModelRM.breadCrumbs(self)
        return [bc[0],bc[-1]]

    def deviceMoveTargets(self):
        """see IManageDevice"""
        mroot = self.getDmdRoot("Monitors")._getOb(self.monitorRootName)
        return filter(lambda x: x != self.id, mroot.objectIds())


    def getDeviceMoveTarget(self, moveTargetName):
        """see IManageDevice"""
        mroot = self.getDmdRoot("Monitors")._getOb(self.monitorRootName)
        return mroot._getOb(moveTargetName)


    def getOrganizerName(self):
        """Return the DMD path of an Organizer without its dmdSubRel names."""
        return self.id

    def setPerformanceMonitor(self, performanceMonitor=None, deviceNames=None, 
                              REQUEST=None):
        """ Provide a method to set performance monitor from any organizer """
        if not performanceMonitor:
            if REQUEST:
                messaging.IMessageSender(self).sendToBrowser(
                    'Error',
                    'No monitor was selected.',
                    priority=messaging.WARNING
                )
            return self.callZenScreen(REQUEST)
        if deviceNames is None:
            if REQUEST:
                messaging.IMessageSender(self).sendToBrowser(
                    'Error',
                    'No devices were selected.',
                    priority=messaging.WARNING
                )
            return self.callZenScreen(REQUEST)
        for devname in deviceNames:
            dev = self.devices._getOb(devname)
            dev.setPerformanceMonitor(performanceMonitor)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Monitor Set',
                'Performance monitor was set to %s.' % performanceMonitor
            )
            if REQUEST.has_key('oneKeyValueSoInstanceIsntEmptyAndEvalToFalse'):
                return REQUEST['message']
            else:
                return self.callZenScreen(REQUEST)

    def rrdPath(self):
        return 'Daemons/%s' % self.id

    def getRRDContextData(self, context):
        context['here'] = self
        context['name'] = self.id
        return context

    def getGraphDefUrl(self, graph, drange=None, template=None):
        """resolve template and graph names to objects 
        and pass to graph performance"""
        if not drange: drange = self.defaultDateRange
        templates = self.getRRDTemplates()
        if template:
            templates = [template]
        if isinstance(graph, basestring):
            for t in templates:
                if hasattr(t.graphDefs, graph):
                    template = t
                    graph = getattr(t.graphDefs, graph)
                    break
        targetpath = self.rrdPath()
        objpaq = self.primaryAq()
        return self.performanceGraphUrl(objpaq, targetpath, template, graph, drange)


InitializeClass(Monitor)
