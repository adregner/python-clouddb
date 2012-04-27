# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb instance module

This code is licensed under the BSD license.  See COPYING for more details.
"""

import os

class Instance(object):
    """
    Instances of this class represent an Instance in the Cloud Database service.
    This is simular to a MySQL environment within whitch you can have multiple
    databases.
    """
    
    def __init__(self):
        """
        Not to be called directaly.  These instances will be created by the 
        Connection class when you create or list the current instances.
        """
        pass
