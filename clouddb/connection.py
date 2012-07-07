# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb connection module

This is your starting point for accessing the Cloud Database service.

This code is licensed under the MIT license.  See COPYING for more details.
"""

from apirequester import APIRequester
from models import *
import consts
import helpers

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
        
        self.client = APIRequester(self.user, self.key, 
            auth_url, "cloudDatabases", self.region, debug=self.debug)
        
        #Database.client = self.client
        #Flavor.client = self.client
        #Instance.client = self.client
        #User.client = self.client

    def __str__(self):
        """
        """
        fq_name = "%s.%s" % (self.__module__, self.__class__.__name__)
        return "<%s object, username=%s, region=%s>" % (fq_name, self.user, self.region)

    def instances(self):
        """
        """
        apiout = self.client.get('/instances')
        return helpers.build_from_list(self, Instance, apiout['instances'])

    def flavors(self):
        """
        """
        apiout = self.client.get('/flavors')
        return helpers.build_from_list(self, Flavor, apiout['flavors'])

    def get_flavor(self, flavor_id):
        """
        """
        return helpers.get_from_id(self, Flavor, flavor_id)

    def get_instance(self, instance_id):
        """untested
        """
        return helpers.get_from_id(self, Instance, instance_id)

    def create_instance(self, name=None, flavor=None, size=None, database=None, user=None, **instance):
        """
        """
        # name
        if name is not None:
            instance['name'] = str(name)

        # ram size of the instance
        if type(flavor) == Flavor:
            instance['flavorRef'] = flavor.bookmark_link
        elif type(flavor) == dict:
            instance['flavorRef'] = self.flavors().find(**flavor)
        elif type(flavor) in (int, str, unicode):
            instance['flavorRef'] = str(flavor)

        # size of the instance
        if size is not None and (type(size) == int or size.isdigit()):
            instance['volume'] = { 'size': str(size) }

        # initial database
        if type(database) in (str, unicode):
            instance['databases'] = [{"name": database}]
        elif type(database) == dict:
            instance['databases'] = [database]

        # initial user
        if type(user) == dict:
            instance['users'] = [user]

        apiresult = self.client.post('/instances', { 'instance': instance })
        return Instance(parent = self, **apiresult['instance'])

    def new_instance(self, **kwargs):
        """alias for create_instance
        """
        return self.create_instance(**kwargs)
