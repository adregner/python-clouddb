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

from clouddb.api.auth import APIAuthenticator
from clouddb import errors

class APIRequester(object):
    """
    This class is used internally by the clouddb project to make requests to an
    HTTPS server in a convient way.
    """
    
    def __init__(self, username, api_key, auth_url, service, region=None, **kwargs):
        """
        """
        debug = int(kwargs.get('debug', 0))
        
        APIAuthenticator(username, api_key, auth_url, service, region)
        self._authenticate(debug=debug)

    @classmethod
    def _authenticate(self, **kwargs):
        APIAuthenticator(**kwargs).get_token()

    @classmethod
    def _build_path(self, path):
        """
        """
        if type(path) in (tuple, list):
            path = "/".join(path)
        return path.strip('/')

    @classmethod
    def request(self, method='GET', path=None, data=None, headers=None, args=None, debug=0):
        """
        """
        # get the authentication info from the singleton
        (auth_token, host, base_path) = APIAuthenticator()()
        
        method = method.upper()
        
        # build the full path to request
        request_path = ''
        if base_path:
            request_path = '/' + base_path
        request_path += '/' + self._build_path(path)
        
        # check that we aren't trying to use data when we can't
        if data and method not in ('POST', 'PUT'):
            raise BadRequest("%s requests cannot contain data" % method)

        # get base headers
        request_headers = {
            'X-Auth-Token': auth_token,
        }
        
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
            client = HTTPSConnection(host)
            client.set_debuglevel(debug)
            client.request(method, request_path, data, request_headers)
            response = client.getresponse()
            #client.close()
            return response

        # first try...
        response = make_request()

        # maybe we need to authenticate again
        if response.status == 401:
            self._authenticate()
            response = make_request()

        return response

    @classmethod
    def handle_response(self, r):
        """
        """
        if r.status < 200 or r.status > 299:
            # TODO : this is probably throwing away some error information
            raise errors.ResponseError(r.status, r.reason)

        read_output = r.read()
        #print repr(r.status)
        #print repr(read_output)
        #print repr(r.getheaders())

        if int(r.getheader('content-length', 1)) == 0:
            return True
        elif r.getheader('content-type', 'text/plain') == "application/json":
            return json_loads(read_output)
        else:
            return read_output

    @classmethod
    def get(self, path, headers=None, args=None, debug=0):
        """
        """
        r = self.request('GET', path, None, headers, args, debug)
        return self.handle_response(r)

    @classmethod
    def post(self, path, data=None, headers=None, args=None, debug=0):
        """
        """
        r = self.request('POST', path, data, headers, args, debug)
        return self.handle_response(r)

    @classmethod
    def delete(self, path, data=None, headers=None, args=None, debug=0):
        """
        """
        r = self.request('DELETE', path, None, headers, args, debug)
        return self.handle_response(r)

    @classmethod
    def put(self, path, data=None, headers=None, args=None, debug=0):
        """
        """
        r = self.request('PUT', path, data, headers, args, debug)
        return self.handle_response(r)


class BadRequest(Exception):
    pass
