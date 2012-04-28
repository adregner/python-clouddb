# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb connection module

This is your starting point for accessing the Cloud Database service.

This code is licensed under the BSD license.  See COPYING for more details.
"""

from apirequester import APIRequester
from models import *
import consts

class Connection(object):
    """
    Represents a connection, or an active session with the Cloud Database API.
    Use this class to create a connection to the service, and to get other
    objects that you can use to perform any required action with the service.
    """
    
    def __init__(self, username, api_key, region, auth_url=None, **kwargs):
        """
        Use this to create your connection to the service with your Rackspace
        Cloud user name and API key, and access the Cloud Databases service in
        the desired region where the service is avaliable. (ORD, DFW, LON).
        
        The auth_url parameter can be used to connect to another compatiable
        service endpoint other then Rackspace.
        """
        self.user = username
        self.key = api_key
        self.region = region.upper()
        
        if not auth_url:
            auth_url = consts.default_authurl
        
        self.debug = int(kwargs.get('debug', 0))
        
        # this is set twice in here, once to authenticate and another for the
        # host the service api endpoint is on
        self.client = None
        
        self.client = APIRequester(self.user, self.key, 
            auth_url, "cloudDatabases", region, debug=self.debug)

    def __str__(self):
        """
        """
        fq_name = "%s.%s" % (self.__module__, self.__class__.__name__)
        return "<%s object, username=%s, region=%s>" % (fq_name, self.user, self.region)

    def instances(self):
        """
        """
        pass
    
    def flavors(self):
        """
        """
        apiout = self.client.get('/flavors')
        flavors = list()
        
        for f in apiout['flavors']:
            flavors.append(Flavor(**f))
        
        return flavors
    
    

