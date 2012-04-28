
"""Primary testing suite for clouddb.connection. """

import unittest
import getpass

from test_clouddb import RAXDB
import clouddb

class ConnectionLists(unittest.TestCase):
    """Testing suite for the lists of things clouddb.connection has."""

    def test_flavors_list(self):
        flavors = RAXDB.flavors()
        self.assertIsInstance(flavors, list)
        self.assertIsInstance(flavors[0], clouddb.models.flavor.Flavor)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ConnectionLists))
    return suite

if __name__ == "__main__":
    unittest.main()
