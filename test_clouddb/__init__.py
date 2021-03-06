
"""Primary testing suite for clouddb

This code is licensed under the MIT license.  See COPYING for more details."""

import getpass
import os
import sys
import unittest

import clouddb

if 'OS_USERNAME' not in os.environ:
    os.environ['OS_USERNAME'] = raw_input("username: ")

if 'OS_PASSWORD' not in os.environ:
    os.environ['OS_PASSWORD'] = getpass.getpass("api key: ")

if 'RAX_REGION' not in os.environ:
    os.environ['RAX_REGION'] = 'DFW'

class BaseTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.raxdb = clouddb.Connection(
            os.environ['OS_USERNAME'], os.environ['OS_PASSWORD'], os.environ['RAX_REGION'])

import test_connection
import test_instance
import test_database_and_user

def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_connection.suite())
    suite.addTest(test_instance.suite())
    suite.addTest(test_database_and_user.suite())
    return suite

if __name__ == "__main__":
    unittest.main()
