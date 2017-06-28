##############################################################################
#
# Copyright (C) Zenoss, Inc. 2017, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################


import unittest

from Products.AdvancedQuery import Eq
from Products.ZenTestCase.BaseTestCase import BaseTestCase
from Products.Zuul.catalog.interfaces import IModelCatalogTool
from Products.Zuul.catalog.model_catalog import ModelCatalogDataManager, SearchParams

from zenoss.modelindex.model_index import SearchParams


class TestModelCatalogTransactions(BaseTestCase):

    def afterSetUp(self):
        super(TestModelCatalogTransactions, self).afterSetUp()
        # Lets change the ModelCatalogTestDataManager with ModelCatalogDataManager
        self.model_catalog = IModelCatalogTool(self.dmd)
        self.data_manager = ModelCatalogDataManager('localhost:8983')
        self.model_catalog.model_catalog_client._data_manager = self.data_manager
        # get a refence to model_index to be able to fo checks bypassing the data manager
        self.model_index = self.data_manager.model_index

    def beforeTearDown(self):
        # we dont need to put back the test data manager since each test creates its own
        pass

    def _get_transaction_state(self):
        tid = self.data_manager._get_tid()
        return self.data_manager._current_transactions.get(tid)

    def _check_uid_is_pending_to_be_indexed(self, uid, tx_state, previousy_committed=False):
        self.assertTrue(uid in tx_state.pending_updates)
        if previousy_committed:
            self.assertTrue(uid in tx_state.indexed_updates)
            self.assertTrue(uid in tx_state.temp_indexed_uids)
        else:
            self.assertTrue(uid not in tx_state.indexed_updates)
            self.assertTrue(uid not in tx_state.temp_indexed_uids)

    def _check_uid_is_temporary_indexed(self, uid, tx_state):
        self.assertTrue(uid in tx_state.indexed_updates)
        self.assertTrue(uid in tx_state.temp_indexed_uids)

    def testDataManager(self):
        tx_state = self._get_transaction_state()
        # before any changes are made, tx_state is None
        self.assertIsNone(tx_state)
        device_class_1 = "device_class_1"
        device_class_2 = "device_class_2"

        # create an organizer
        dc_1 = self.dmd.Devices.createOrganizer(device_class_1)
        tx_state = self._get_transaction_state()
        dc_1_uid = dc_1.idx_uid()

        # Some tx_state checks
        self.assertIsNotNone(tx_state)
        self.assertTrue( len(tx_state.pending_updates) == 1 )
        self.assertTrue( len(tx_state.indexed_updates) == 0 )
        self.assertTrue( len(tx_state.temp_indexed_uids) == 0 )
        self.assertTrue( len(tx_state.temp_deleted_uids) == 0 )

        # The new organizer index update should have been buffered in tx_state
        self._check_uid_is_pending_to_be_indexed(dc_1_uid, tx_state)

        # A search with commit_dirty=False should not find the new device organizer
        search_result = self.model_catalog.search(query=Eq("uid", dc_1_uid), commit_dirty=False)
        self.assertEquals(search_result.total, 0)

        # A search with commit_dirty=True must find the new device organizer
        search_result = self.model_catalog.search(query=Eq("uid", dc_1_uid), commit_dirty=True)
        self.assertEquals(search_result.total, 1)

        # the tx_state object should have been updated appropiately
        self._check_uid_is_temporary_indexed(dc_1_uid, tx_state)
        self.assertTrue(dc_1_uid not in tx_state.pending_updates)
        self.assertTrue(dc_1_uid not in tx_state.temp_deleted_uids)
        
        # create another organizer
        dc_2 = self.dmd.Devices.createOrganizer(device_class_2)
        dc_2_uid = dc_2.idx_uid()

        # check tx_state has been updated accordinly
        tx_state = self._get_transaction_state()
        self._check_uid_is_pending_to_be_indexed(dc_2_uid, tx_state)

        # search for both device classes with commit_dirty=False, it should only return dc_1_uid



def test_suite():
    return unittest.TestSuite((unittest.makeSuite(TestModelCatalogTransactions),))


if __name__=="__main__":
    unittest.main(defaultTest='test_suite')
