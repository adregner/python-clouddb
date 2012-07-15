
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
    os.environ['RAX_REGION'] = raw_input("region (ord, dfw): ")

import test_connection
import test_instance

def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_connection.suite())
    suite.addTest(test_instance.suite())
    return suite

if __name__ == "__main__":
    unittest.main()
