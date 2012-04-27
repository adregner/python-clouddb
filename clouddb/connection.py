# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb connection module

This is your starting point for accessing the Cloud Database service.

This code is licensed under the BSD license.  See COPYING for more details.
"""

import os

class Connection(object):
    """
    Represents a connection, or an active session with the Cloud Database API.
    Use this class to create a connection to the service, and to get other
    objects that you can use to perform any required action with the service.
    """
    
    def __init__(self, username, api_key, region, auth_url=None):
        """
        Use this to create your connection to the service with your Rackspace
        Cloud user name and API key, and access the Cloud Databases service in
        the desired region where the service is avaliable. (ORD, DFW, LON).
        
        The auth_url parameter can be used to connect to another compatiable
        service endpoint other then Rackspace.
        """
        pass
