
"""Primary testing suite for clouddb.connection.

This code is licensed under the MIT license.  See COPYING for more details."""

import unittest

from test_clouddb import RAXDB
import clouddb

class ConnectionLists(unittest.TestCase):
    """Testing suite for the lists of things clouddb.connection has."""

    def test_flavors_list(self):
        flavors = RAXDB.flavors()
        self.assertIsInstance(flavors, list)
        self.assertGreater(len(flavors), 0)
        self.assertIsInstance(flavors[0], clouddb.models.flavor.Flavor)

    def test_instances_list(self):
        instances = RAXDB.instances()
        self.assertIsInstance(instances, list)
        self.assertGreater(len(instances), 0)
        self.assertIsInstance(instances[0], clouddb.models.instance.Instance)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ConnectionLists))
    return suite

if __name__ == "__main__":
    unittest.main()
