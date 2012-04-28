# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb database module

This code is licensed under the BSD license.  See COPYING for more details.
"""

import os

class Database(object):
    """
    Instances of this class represent a database in the Cloud Database service.
    """
    
    def __init__(self):
        """
        Not to be called directaly.  These instances will be created by the 
        Connection class when you create or list your databases.
        """
        pass
