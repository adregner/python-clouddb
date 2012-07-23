
"""Primary testing suite for clouddb.models.instance.

This code is licensed under the MIT license.  See COPYING for more details."""

import time
import unittest

import clouddb
import test_clouddb

CLOUDDB_TEST_INSTANCE_NAME = "testsuite-dbu-%d" % time.time()
CLOUDDB_TEST_DATABASE_NAME = "testdb_%d_%%d" % time.time()
CLOUDDB_TEST_DATABASE_I = 1

CLOUDDB_TEST_INSTANCE_OBJECT = None

class InstanceMakerBaseTestCase(test_clouddb.BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(InstanceMakerBaseTestCase, self).__init__(*args, **kwargs)
        if CLOUDDB_TEST_INSTANCE_OBJECT is None:
            CLOUDDB_TEST_INSTANCE_OBJECT = self.raxdb.create_instance({
                'name': CLOUDDB_TEST_INSTANCE_NAME,
                'flavorRef': 1,
                'volume': {'size': 1},
            }, wait=True)
        
        self.instance = CLOUDDB_TEST_INSTANCE_OBJECT
        self.assertIsInstance(self.instance, clouddb.models.instance.Instance)
        self.assertEqual(self.instance['status'], "ACTIVE")

class StartWithNoDatabases(InstanceMakerBaseTestCase):
    def test_create_database(self):
        dbs = self.instance.databases()
        self.assertIsInstance(dbs, list)
        self.assertEqual(len(dbs), 0)

class CreateDatabases(InstanceMakerBaseTestCase):
    def test_create_database(self):
        self.instance.create_database(CLOUDDB_TEST_DATABASE_NAME % 1)
        self.assertEqual(len(self.instance.databases()), 1)
        self.instance.create_database([CLOUDDB_TEST_DATABASE_NAME % 2, CLOUDDB_TEST_DATABASE_NAME % 3])
        self.assertEqual(len(self.instance.databases()), 3)

class StartWithNoUsers(InstanceMakerBaseTestCase):
    def test_create_database(self):
        us = self.instance.users()
        self.assertIsInstance(us, list)
        self.assertEqual(len(us), 0)

class CreateUsers(InstanceMakerBaseTestCase):
    def test_create_users(self):
        self.instance.create_user("userA", "password123")
        self.assertEqual(len(self.instance.users()), 1)
        self.instance.create_user("userB", "password123", [CLOUDDB_TEST_DATABASE_NAME % 1, CLOUDDB_TEST_DATABASE_NAME % 2])
        self.assertEqual(len(self.instance.users()), 2)

class DeleteUsers(InstanceMakerBaseTestCase):
    def test_delete_users(self):
        self.assertEqual(len(self.instance.users()), 2)
        
        #delete a user by GETing it
        user = self.instance.get_user("userB")
        self.assertIsInstance(user, clouddb.User)
        user.delete()
        self.assertEqual(len(self.instance.users()), 1)
        
        #make sure we know what we have left
        self.assertEqual(self.instance.users()[0]['name'], "userA")
        
        #delete the other user outright
        self.instance.delete_user("userA")
        self.assertEqual(len(self.instance.users()), 0)

class DeleteDatabases(InstanceMakerBaseTestCase):
    def test_create_database(self):
        self.assertEqual(len(self.instance.databases()), 3)
        
        #delete a database by GETing it
        db = self.instance.get_database(CLOUDDB_TEST_DATABASE_NAME % 1)
        self.assertIsInstance(db, clouddb.Database)
        db.delete()
        self.assertEqual(len(self.instance.databases()), 2)
        
        #make sure we know what we have left
        self.assertEqual(self.instance.databases()[0]['name'], CLOUDDB_TEST_DATABASE_NAME % 2)
        self.assertEqual(self.instance.databases()[1]['name'], CLOUDDB_TEST_DATABASE_NAME % 3)
        
        #delete the other user outright
        self.instance.delete_database(CLOUDDB_TEST_DATABASE_NAME % 2)
        self.instance.delete_database(CLOUDDB_TEST_DATABASE_NAME % 3)
        self.assertEqual(len(self.instance.databases()), 0)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StartWithNoDatabases))
    suite.addTest(unittest.makeSuite(CreateDatabases))
    suite.addTest(unittest.makeSuite(InstanceListGet))
    suite.addTest(unittest.makeSuite(InstanceDestroy))
    suite.addTest(unittest.makeSuite(InstanceListFinal))
    return suite

if __name__ == "__main__":
    unittest.main()
