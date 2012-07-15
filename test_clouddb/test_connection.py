
"""Primary testing suite for clouddb.connection.

This code is licensed under the MIT license.  See COPYING for more details."""

import os
import unittest

import clouddb

class ConnectionLists(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ConnectionLists, self).__init__(*args, **kwargs)
        self.raxdb = clouddb.Connection(
            os.environ['OS_USERNAME'], os.environ['OS_PASSWORD'], os.environ['RAX_REGION'])

    def test_logged_in(self):
        self.assertIsInstance(self.raxdb, clouddb.connection.Connection)

class FlavorVerification(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(FlavorVerification, self).__init__(*args, **kwargs)
        self.raxdb = clouddb.Connection(
            os.environ['OS_USERNAME'], os.environ['OS_PASSWORD'], os.environ['RAX_REGION'])

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
