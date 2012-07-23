
"""Primary testing suite for clouddb.models.instance.

This code is licensed under the MIT license.  See COPYING for more details."""

import time
import unittest

import clouddb
import test_clouddb

CLOUDDB_TEST_INSTANCE_OBJECT = None
CLOUDDB_TEST_BASELINE_INSTANCE_COUNT = None
CLOUDDB_TEST_INSTANCE_NAME = "testsuite-ci-%d" % time.time()

class InstanceBaseline(test_clouddb.BaseTestCase):
    def test_instance_list_baseline(self):
        instances = self.raxdb.instances()
        self.assertIsInstance(instances, list)
        test_clouddb.test_instance.CLOUDDB_TEST_BASELINE_INSTANCE_COUNT = len(instances)

class InstanceCreate(test_clouddb.BaseTestCase):
    def test_create_instance(self):
        test_clouddb.test_instance.CLOUDDB_TEST_INSTANCE_OBJECT = \
            self.raxdb.create_instance(CLOUDDB_TEST_INSTANCE_NAME, 1, 1, wait=True)
        self.assertIsInstance(test_clouddb.test_instance.CLOUDDB_TEST_INSTANCE_OBJECT, 
            clouddb.models.instance.Instance)

class InstanceListGet(test_clouddb.BaseTestCase):
    def test_instance_list(self):
        instances = self.raxdb.instances()
        self.assertIsInstance(instances, list)
        self.assertEqual(len(instances),
            test_clouddb.test_instance.CLOUDDB_TEST_BASELINE_INSTANCE_COUNT + 1)
        self.assertIsInstance(instances[-1], clouddb.models.instance.Instance)

class InstanceDestroy(test_clouddb.BaseTestCase):
    def test_instance_remove(self):
        test_clouddb.test_instance.CLOUDDB_TEST_INSTANCE_OBJECT.delete(wait=True)

class InstanceListFinal(test_clouddb.BaseTestCase):
    def test_instance_list_baseline_again(self):
        instances = self.raxdb.instances()
        self.assertEqual(len(instances),
            test_clouddb.test_instance.CLOUDDB_TEST_BASELINE_INSTANCE_COUNT)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InstanceBaseline))
    suite.addTest(unittest.makeSuite(InstanceCreate))
    suite.addTest(unittest.makeSuite(InstanceListGet))
    suite.addTest(unittest.makeSuite(InstanceDestroy))
    suite.addTest(unittest.makeSuite(InstanceListFinal))
    return suite

if __name__ == "__main__":
    unittest.main()
