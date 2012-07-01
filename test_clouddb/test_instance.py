
"""Primary testing suite for clouddb.models.instance.

This code is licensed under the MIT license.  See COPYING for more details."""

import unittest

from test_clouddb import RAXDB
import clouddb

INSTANCE = RAXDB.instances()[0]

class InstanceOps(unittest.TestCase):
    """Testing suite for the lists of things clouddb.connection has."""

    def test_databases_list(self):
        databases = INSTANCE.databases()
        self.assertIsInstance(databases, list)
        self.assertGreater(len(databases), 0)
        self.assertIsInstance(databases[0], clouddb.models.database.Database)

    def test_users_list(self):
        users = INSTANCE.users()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        self.assertIsInstance(users[0], clouddb.models.user.User)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InstanceOps))
    return suite

if __name__ == "__main__":
    unittest.main()
