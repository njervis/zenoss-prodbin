import unittest
import transaction
import zope.component

from Testing import ZopeTestCase
from Testing.ZopeTestCase.layer import ZopeLite
from Products.ZenModel.interfaces import IDataRoot
from Products.ZenTestCase.BaseTestCase import BaseTestCase
from Products.ZenTestCase.BaseTestCase import ZenossTestCaseLayer

class ZuulServiceTestCase(BaseTestCase):
    def test_interfaces(self):
        raise NotImplementedError("You're not verifying that the"
                                  " class correctly implements its"
                                  " interfaces.")

class EventTestLayer(ZenossTestCaseLayer):

    _evids = None

    @classmethod
    def setUp(cls):
        ZenossTestCaseLayer.setUp()
        import Products
        from Products.ZenUtils.ZCmdBase import ZCmdBase
        zodb = ZCmdBase(noopts=True)
        zem = zodb.dmd.ZenEventManager
        zope.component.provideUtility(zodb.dmd, provides=IDataRoot)
        cls.zem = zem
        cls._evids = []

    @classmethod
    def tearDown(cls):
        ZenossTestCaseLayer.tearDown()
        if not cls._evids:
            return
        evids = ','.join("'%s'" % evid for evid in cls._evids)
        conn = cls.zem.connect()
        try:
            curs = conn.cursor()
            curs.execute('DELETE FROM status WHERE evid in (%s)' % evids)
        finally:
            cls.zem.close(conn)


from Products.ZenEvents.Event import Event

class EventTestCase(unittest.TestCase):

    layer = EventTestLayer

    def sendEvent(self, **kwargs):
        evt = Event()
        defaults = dict(
            device='localhost',
            eventClass="/TestEvent",
            summary='Test event generated by %s' %
                        self.__class__.__name__,
            severity=4)
        defaults.update(kwargs)
        for k,v in defaults.items():
            setattr(evt, k, v)

        evid = self.layer.zem.sendEvent(evt)
        self.layer._evids.append(evid)
        return evid

    def clearCache(self):
        self.layer.zem.clearCache()
        self.layer.zem.manage_clearCache()

