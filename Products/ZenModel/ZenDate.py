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

from Globals import Persistent
from DateTime import DateTime
from Products.ZenUtils import Time

class ZenDate(Persistent):
    """
    DEPRECATED wraper so that date sets on device don't provoke entire object
    store
    """
    
    def __init__(self, date=None):
        self.setDate(date)
        
    def setDate(self, date=None):
        if date == None: date = DateTime()
        if isinstance(date, basestring):
            date = DateTime(date)
        self.date = date

    def __float__(self):
        return float(self.date)

    def getDate(self):
        return self.date
   
    def getString(self):
        """Date in format 2006/09/13 12:16:06.000
        """
        return Time.LocalDateTime(self.date.timeTime())

    def getStringSecsResolution(self):
        """Date in format 2006/09/13 12:16:06
        """
        return Time.LocalDateTimeSecsResolution(self.date.timeTime())
