# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb flavor module

This code is licensed under the BSD license.  See COPYING for more details.
"""

import os

class Flavor(object):
    """
    Instances of this class represent a flavor of a database instance in the
    Cloud Databases service.
    """
    
    def __init__(self):
        """
        Not to be called directaly.  These instances will be created by the 
        Connection class when you create or list the avaliable flavors.
        """
        pass
