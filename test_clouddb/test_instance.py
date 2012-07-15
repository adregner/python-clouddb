
"""Primary testing suite for clouddb.models.instance.

This code is licensed under the MIT license.  See COPYING for more details."""

import os
import time
import unittest

import clouddb

CLOUDDB_TEST_BASELINE_INSTANCE_COUNT = None

class InstanceCreate(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(InstanceCreate, self).__init__(*args, **kwargs)
        self.raxdb = clouddb.Connection(
            os.environ['OS_USERNAME'], os.environ['OS_PASSWORD'], os.environ['RAX_REGION'])

    def test_instance_list_baseline(self):
        instances = self.raxdb.instances()
        self.assertIsInstance(instances, list)
        CLOUDDB_TEST_BASELINE_INSTANCE_COUNT = len(instances)

    def test_create_instance(self):
        self.raxdb.create_instance(
            name = "testsuite-%d" % time.time(),
        )

class InstanceListGet(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(InstanceListGet, self).__init__(*args, **kwargs)
        self.raxdb = clouddb.Connection(
            os.environ['OS_USERNAME'], os.environ['OS_PASSWORD'], os.environ['RAX_REGION'])

    def test_instance_list(self):
        instances = self.raxdb.instances()
        self.assertIsInstance(instances, list)
        self.assertGreater(len(instances), CLOUDDB_TEST_BASELINE_INSTANCE_COUNT)
        self.assertIsInstance(instances[0], clouddb.models.instance.Instance)

class InstanceDestroy(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(InstanceDestroy, self).__init__(*args, **kwargs)
        self.raxdb = clouddb.Connection(
            os.environ['OS_USERNAME'], os.environ['OS_PASSWORD'], os.environ['RAX_REGION'])

    def test_instance_remove(self):
        pass

    def test_instance_list_baseline_again(self):
        instances = self.raxdb.instances()
        self.assertEqual(len(instances), CLOUDDB_TEST_BASELINE_INSTANCE_COUNT)

def suite():
    suite = unittest.TestSuite()
    #suite.addTest(unittest.makeSuite(InstanceCreate))
    #suite.addTest(unittest.makeSuite(InstanceListGet))
    #suite.addTest(unittest.makeSuite(InstanceDestroy))
    return suite

if __name__ == "__main__":
    unittest.main()
