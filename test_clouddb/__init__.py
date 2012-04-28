
"""Primary testing suite for clouddb"""

import sys
import os
import unittest
import getpass

import clouddb

username = os.environ['OS_USERNAME'] if 'OS_USERNAME' in os.environ else raw_input("username: ")
api_key = os.environ['OS_PASSWORD'] if 'OS_PASSWORD' in os.environ else getpass.getpass("api key: ")

RAXDB = clouddb.Connection(username, api_key, raw_input("region (ord, dfw): "))

import test_connection

def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_connection.suite())
    return suite

if __name__ == "__main__":
    unittest.main()
