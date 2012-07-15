# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
Generic module to get an authentication token for an API

This code is licensed under the MIT license.  See COPYING for more details.
"""

from httplib import HTTPSConnection
from urlparse import urlparse

try:
    from json import loads as json_loads
except ImportError:
    from simplejson import loads as json_loads

class APIAuthenticator(object):
    """Stateful singleton that logs into and tracks API access."""
    __instance = None
    __shared_state = {}
    __initialized = False

    debug = 0

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(APIAuthenticator, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        self.__dict__ = self.__shared_state

        if 'debug' in kwargs:
            self.debug = kwargs['debug']
            del kwargs['debug']

        if self.__initialized:
            return
        self.__initialized = True

        keys = ('username', 'api_key', 'auth_url', 'service', 'region')
        keys = zip(range(len(keys)), keys)

        for n, key in keys:
            try:
                setattr(self, key, args[n])
            except IndexError:
                setattr(self, key, kwargs[key])

    def __call__(self):
        return (self._token, self._service_host, self._service_path)

    def get_token(self):
        """Login to an API capturing the auth token for this session.

        username :: 
        api_key :: 
        auth_url :: 
        service :: 
        region :: 
        """

        # hit the API and find the token
        (scheme, auth_host, auth_path, params, query, frag) = urlparse(self.auth_url)

        if scheme != 'https':
            raise Exception("We only support https")

        self.client = HTTPSConnection(auth_host)
        self.client.set_debuglevel(self.debug)

        request_headers = {
            'Content-type': 'application/json'
        }

        auth_data = """{"auth": {"RAX-KSKEY:apiKeyCredentials": {
            "username": "%s", "apiKey": "%s"
        }}}""" % (self.username, self.api_key)

        self.client.request('POST', auth_path, auth_data, request_headers)

        auth_response = self.client.getresponse()

        if auth_response.status != 200:
            # TODO : proper error
            raise Exception("Authentication failure")

        auth_response = json_loads(auth_response.read())

        self._token = auth_response['access']['token']['id']

        # find this service in the catalog
        for endpts in auth_response['access']['serviceCatalog']:
            if endpts['name'] == self.service:
                service_points = endpts['endpoints']
                break

        # pick our region
        if not self.region:
            service_url = service_points[0]['publicURL']
        else:
            service_url = None
            for endpoint in service_points:
                if endpoint['region'] == self.region:
                    service_url = endpoint['publicURL']
                    break
            if service_url is None:
                # TODO : proper error
                raise Exception("%s region is not avaliable." % self.region)

        (scheme, self._service_host, self._service_path, params, query, frag) = \
            urlparse(service_url)

        self.client.close()
        self._service_path = self._service_path.strip('/')
