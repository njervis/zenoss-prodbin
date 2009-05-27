###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

"""
test that the do nothing crypter can be stored in the database and that it
simply returns the parameter passed in to the two methods
"""

from unittest import TestCase, TestSuite, makeSuite
from Products.ZenTestCase.BaseTestCase import BaseTestCase
from Products.ZenModel.Crypter import Crypter

class CrypterTest(TestCase):
        
    def testEncryt(self):
        "test that encrypt returns the string that was passed in"
        self.assertEqual('foo', Crypter().encrypt('foo'))
        
    def testDecrypt(self):
        "test that decrypt returns the string that was passed in"
        self.assertEqual('bar', Crypter().decrypt('bar'))
        
class StoreTest(BaseTestCase):
    "make sure an instance of the crypter can be stored"
    
    def runTest(self):
        id = 'testCrypter'
        self.dmd._setObject(id, Crypter(id))
        crypter = self.dmd.findChild(id)
        self.assertEqual('foo', crypter.encrypt('foo'))
        self.assertEqual('bar', crypter.decrypt('bar'))
        
def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(CrypterTest))
    suite.addTest(makeSuite(StoreTest))
    return suite
