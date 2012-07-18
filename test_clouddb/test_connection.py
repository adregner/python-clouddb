
"""Primary testing suite for clouddb.connection.

This code is licensed under the MIT license.  See COPYING for more details."""

import unittest

import clouddb
import test_clouddb

class ConnectionLists(test_clouddb.BaseTestCase):
    def test_logged_in(self):
        self.assertIsInstance(self.raxdb, clouddb.connection.Connection)

class FlavorVerification(test_clouddb.BaseTestCase):
    def test_flavors_list(self):
        flavors = self.raxdb.flavors()
        self.assertIsInstance(flavors, list)
        self.assertGreater(len(flavors), 0)
        self.assertIsInstance(flavors[0], clouddb.models.flavor.Flavor)
    def test_get_flavor(self):
        the_flavor = clouddb.models.flavor.Flavor.find(ram=1024)
        self.assertIsInstance(the_flavor, clouddb.models.flavor.Flavor)
        self.assertEqual(the_flavor['ram'], 1024)
        self.assertEqual(the_flavor['name'], 'm1.small')
        self.assertEqual(the_flavor['id'], 2)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ConnectionLists))
    suite.addTest(unittest.makeSuite(FlavorVerification))
    return suite

if __name__ == "__main__":
    unittest.main()
