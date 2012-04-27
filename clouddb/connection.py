# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb connection module

This is your starting point for accessing the Cloud Database service.

This code is licensed under the BSD license.  See COPYING for more details.
"""

from urlparse import urlparse

from requester import Requester
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
        self.token = None
        self.region = region.upper()
        
        if not auth_url:
            auth_url = consts.default_authurl
        
        (scheme, auth_netloc, auth_path, params, query, frag) = urlparse(auth_url)
        
        self.debug = int(kwargs.get('debug', 0))
        
        # this is set twice in here, once to authenticate and another for the
        # host the service api endpoint is on
        self.client = None
        
        self._authenticate(auth_netloc, auth_path)

    def _authenticate(self, auth_host, auth_path):
        """
        """
        client = Requester(auth_host)
        auth_response = client.request('POST', auth_path, data={
            'username': self.user,
            'key': self.key
        })

    def _request(self, method, path, data='', headers=None, params=None):
        """
        """
        pass
