#!/usr/bin/python
##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


#
# Contained below is the class that tests elements located under
# the "Event Manager" Browse By subheading.
#
# Adam Modlin and Nate Avers
#

import unittest

from SelTestBase import SelTestBase

class TestEventManager(SelTestBase):
    """Defines a class that runs tests under the Event Manager heading"""

    def testRefreshEventSchema(self):
        """Test refreshing the event schema"""
        self.waitForElement("link=Event Manager")
        self.selenium.click("link=Event Manager")
        self.selenium.wait_for_page_to_load(self.WAITTIME)
        self.waitForElement("link=Refresh Event Schema...")
        self.selenium.click("link=Refresh Event Schema...")    
        self.waitForElement("manage_refreshConversions:method")
        self.selenium.click("manage_refreshConversions:method")
        self.selenium.wait_for_page_to_load(self.WAITTIME)
        self.waitForElement("manage_editEventManager:method")
        self.selenium.click("manage_editEventManager:method")
        
    def testClearEventCache(self):
        """Test clearing the event cache"""
        self.waitForElement("link=Event Manager")
        self.selenium.click("link=Event Manager")
        self.selenium.wait_for_page_to_load(self.WAITTIME)
        self.waitForElement("link=Clear Event Cache...")
        self.selenium.click("link=Clear Event Cache...")
        self.waitForElement("manage_clearCache:method")
        self.selenium.click("manage_clearCache:method")
        self.selenium.wait_for_page_to_load(self.WAITTIME)
        self.waitForElement("manage_editEventManager:method")
        self.selenium.click("manage_editEventManager:method")
        
    def testClearAllHeartbeats(self):
        """Test clearing all heartbeats"""
        self.waitForElement("link=Event Manager")
        self.selenium.click("link=Event Manager")
        self.selenium.wait_for_page_to_load(self.WAITTIME)
        self.waitForElement("link=Clear All Heartbeats...")
        self.selenium.click("link=Clear All Heartbeats...")
        self.waitForElement("manage_clearHeartbeats:method")
        self.selenium.click("manage_clearHeartbeats:method")
        self.selenium.wait_for_page_to_load(self.WAITTIME)
        self.waitForElement("manage_editEventManager:method")
        self.selenium.click("manage_editEventManager:method")
        
    def testEditEventManager(self):
        """Test editing event database properties"""
        self.waitForElement("link=Event Manager")
        self.selenium.click("link=Event Manager")
        self.selenium.wait_for_page_to_load(self.WAITTIME)
        #Edit the Event Manager
        self.waitForElement("history_clearthresh:int")
        self.selenium.type("timeout:int", "19")
        self.selenium.type("clearthresh:int", "19")
        self.selenium.type("history_timeout:int", "299")
        self.selenium.type("history_clearthresh:int", "19")
        self.waitForElement("manage_editEventManager:method")
        self.selenium.click("manage_editEventManager:method")
        self.selenium.wait_for_page_to_load(self.WAITTIME)
        #Change back to initial values
        self.waitForElement("history_clearthresh:int")
        self.waitForElement("manage_editEventManager:method")
        self.selenium.type("timeout:int", "20")
        self.selenium.type("clearthresh:int", "20")
        self.selenium.type("history_timeout:int", "300")
        self.selenium.type("history_clearthresh:int", "20")
        self.waitForElement("manage_editEventManager:method")
        self.selenium.click("manage_editEventManager:method")    
        
    def testEditFields(self):
        """Test editing the fields tab"""    
        self.waitForElement("link=Event Manager")
        self.selenium.click("link=Event Manager")
        self.selenium.wait_for_page_to_load(self.WAITTIME)
        self.waitForElement("link=Fields")
        self.selenium.click("link=Fields")
        self.selenium.wait_for_page_to_load(self.WAITTIME)
        self.waitForElement("zmanage_editProperties:method")
        self.selenium.click("zmanage_editProperties:method")

# Method is currently broken. See comment below for details.    
#    def testCommands(self):
#        """Test adding, editing and deleting commands"""
#        self.waitForElement("link=Event Manager")
#        self.selenium.click("link=Event Manager")
#        self.selenium.wait_for_page_to_load(self.WAITTIME)
#        self.waitForElement("link=Commands")
#        self.selenium.click("link=Commands")
#        self.selenium.wait_for_page_to_load(self.WAITTIME)
#        self.waitForElement("manage_addCommand:method")
#        self.selenium.type("id", "testingString")
#        self.selenium.click("manage_addCommand:method")
#        getByValue ("ids:list", "testingString", formName="clauseForm")
#        self.waitForElement("manage_deleteCommands:method")
#        # Selenium is unable to find this command for an unknown reason.
#        self.selenium.click("manage_deleteCommands:method")
    
    
    
if __name__ == "__main__":
    unittest.main()
