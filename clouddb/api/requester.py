# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
Generic module to make HTTP(S) requests to a server.

This code is licensed under the MIT license.  See COPYING for more details.
"""

from urlparse import urlparse
from httplib import HTTPSConnection
from urllib import urlencode
import socket

try:
    from json import loads as json_loads
    from json import dumps as json_dumps
except ImportError:
    from simplejson import loads as json_loads
    from simplejson import dumps as json_dumps

import clouddb.errors

class APIRequester(object):
    """
    This class is used internally by the clouddb project to make requests to an
    HTTPS server in a convient way.
    """
    
    def __init__(self, username, api_key, auth_url, service, region, **kwargs):
        """
        """
        self.debug = int(kwargs.get('debug', 0))
        
        self.base_path = ""
        self.base_headers = {}
        self.tenant_id = None
        self.client = None
        
        (scheme, auth_host, auth_path, params, query, frag) = urlparse(auth_url)
        
        if scheme != 'https':
            raise Exception("We only support https")
        
        self.user = username
        self.key = api_key
        self.auth_host = auth_host
        self.auth_path = auth_path
        self.service = service
        self.region = region.upper()
        
        self._current_host = self.auth_host
        self._authenticate()

    def _setup(self):
        """
        """
        if self.client is not None:
            self.client.close()
        
        self.client = HTTPSConnection(self._current_host)
        self.client.set_debuglevel(self.debug)

    def _authenticate(self):
        """
        """
        
        auth_data = self.post(self.auth_path, {
            'auth': {
                'RAX-KSKEY:apiKeyCredentials': {
                    'username': self.user, 'apiKey': self.key
        }}})
        
        self.set_base_header({
            'X-Auth-Token': auth_data['access']['token']['id']
        })
        
        self.tenant_id = auth_data['access']['token']['tenant']['id']
        
        # TODO : save the expires timestamp of the token and reauth when needed
        
        # find this service in the catalog
        for endpts in auth_data['access']['serviceCatalog']:
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
        
        (scheme, self.host, path, params, query, frag) = urlparse(service_url)
        
        # establish settings and connection for the service endpoint
        self._current_host = self.host
        self.set_base_path(path)

    def set_base_header(self, header, value=None):
        """
        """
        # set multiple headers
        if type(header) in (dict,) and len(header) > 0:
            for k, v in header.items():
                self.set_base_header(k, v)

        # set this one header, from a list or strings
        else:
            if type(header) in (tuple, list) and len(header) >= 2:
                header, value = header[0], header[1]

            self.base_headers[header.title()] = value

    def get_base_headers(self):
        """
        """
        return self.base_headers

    def delete_base_header(self, header):
        """
        """
        if header in self.base_headers:
            del self.base_headers[header.title()]

    def _build_path(self, path):
        """
        """
        if type(path) in (tuple, list):
            path = "/".join(path)
        return path.strip('/')

    def set_base_path(self, path):
        """
        """
        self.base_path = self._build_path(path)

    def get_base_path(self):
        """
        """
        return self.base_path

    def request(self, method='GET', path=None, data=None, headers=None, args=None):
        """
        """
        method = method.upper()
        
        # build the full path to request
        request_path = ''
        if self.get_base_path() is not None:
            request_path = '/' + self.get_base_path()
        request_path += '/' + self._build_path(path)
        
        # check that we aren't trying to use data when we can't
        if data and method not in ('POST', 'PUT'):
            raise BadRequest("%s requests cannot contain data" % method)

        # get base headers
        request_headers = self.base_headers.copy()
        
        # don't a type when there is no content
        if not data and 'Content-type' in request_headers:
            del request_headers['Content-type']
        
        # merge base headers and supplied headers
        if headers:
            request_headers.update(headers)

        # encode data if needed
        if data and type(data) != str:
            data = json_dumps(data)
            request_headers['Content-type'] = "application/json"
        
        # append url arguments if given
        if args:
            request_path += '?' + urlencode(args)
        
        # this is how we make a request
        def make_request():
            # TODO : this could be better if we were brave enough to handle keep-alives
            self._setup()
            self.client.request(method, request_path, data, request_headers)
            return self.client.getresponse()
        
        try:
            # first try...
            response = make_request()
        except (socket.error, IOError):
            # maybe we just lost the socket, try again
            self._setup()
            response = make_request()
        
        # maybe we need to authenticate again
        if response.status == 401:
            self._authenticate()
            response = make_request()
        
        return response
    
    def handle_response(self, r):
        """
        """
        if r.status < 200 or r.status > 299:
            # TODO : this is probably throwing away some error information
            raise errors.ResponseError(r.status, r.reason)
        
        read_output = r.read()
        
        if int(r.getheader('content-length', 1)) == 0:
            return True
        elif r.getheader('content-type', 'text/plain') == "application/json":
            return json_loads(read_output)
        else:
            return read_output
    
    def get(self, path, headers=None, args=None):
        """
        """
        r = self.request('GET', path, None, headers, args)
        
        return self.handle_response(r)
    
    def post(self, path, data=None, headers=None, args=None):
        """
        """
        r = self.request('POST', path, data, headers, args)
        
        return self.handle_response(r)
    
    def delete(self, path, data=None, headers=None, args=None):
        """
        """
        r = self.request('DELETE', path, None, headers, args)
        
        return self.handle_response(r)
    
    def put(self, path, data=None, headers=None, args=None):
        """
        """
        r = self.request('PUT', path, data, headers, args)
        
        return self.handle_response(r)


class BadRequest(Exception):
    pass
