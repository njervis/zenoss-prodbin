###############################################################################
#
#   Copyright (c) 2004 Zentinel Systems. 
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
###############################################################################

import cgi

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Event import Event

class ZEvent(Event):
    """
    Event that lives in the zope context has zope security mechanisms and
    url back to event manager
    """
    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")
 
    def __init__(self, manager, fields, data):
        Event.__init__(self)
        self.updateFromFields(fields, data)
        self._zem = manager.getId()
        self._baseurl = manager.absolute_url_path()
 

    def getDataListWithLinks(self, fields):
        """return a list of data elements that map to the fields parameter.
        """
        data = []
        for field in fields:
            value = getattr(self, field)
            if field == "device":
                value = "<a href='/zport/dmd/deviceSearchResults?query=%s'>"\
                        "%s</a>" % (value, value)
            elif field == 'eventClass':
                value = "<a href='/zport/dmd/Events%s'>%s</a>" % (value,value)
            elif field == 'summary' or field == 'message':
                value = cgi.escape(value)
            data.append(value)
        return data


    def getEventDetailHref(self):
        """build an href to call the detail of this event"""
        return "%s/viewEventFields?evid=%s" % (self._baseurl, self.evid)


    def getCssClass(self):
        """return the css class name to be used for this event.
        """
        value = self.severity < 0 and "unknown" or self.severity
        acked = self.eventState > 0 and "acked" or "noack"
        return "zenevents_%s_%s" % (value, acked)

    def zem(self):
        """return the id of our manager.
        """
        return self._zem

InitializeClass(ZEvent)
