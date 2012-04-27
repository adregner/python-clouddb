# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
Generic module to make HTTP(S) requests to a server.

This code is licensed under the BSD license.  See COPYING for more details.
"""

from httplib import HTTPSConnection
from urllib import urlencode

try:
    from json import loads as json_loads
except ImportError:
    from simplejson import loads as json_loads

import errors

class Requester(object):
    """
    This class is used internally by the clouddb project to make requests to an
    HTTPS server in a convient way.
    """
    
    def __init__(self, host, **kwargs):
        """
        """
        self.host = host
        self.debug = int(kwargs.get('debug', 0))
        
        self.base_path = "/"
        self.base_headers = {}
        
        self._client_setup()
        self._authenticate()

    def _setup(self):
        """
        """
        self.client = HTTPSConnection(self.host)
        self.client.set_debuglevel(self.debug)

    def _authenticate(self):
        """
        """
        pass

    def set_base_header(self, header, value):
        """
        """
        
        # set multiple headers
        if type(header) in (dict,) and len(header) > 0:
            for k, v in header.items():
                self.set_header(k, v)

        # set this one header, from a list or strings
        else:
            if type(header) in (tuple, list) and len(header) >= 2:
                header, value = header[0], header[1]

            self.base_headers[header.title()] = value

    def get_base_headers(self):
        """
        """
        return self.headers

    def delete_base_header(self, header):
        """
        """
        if header in self.headers:
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
        path = '/' + self.get_base_path() + '/' + self._build_path(path)
        
        # check that we aren't trying to use data when we can't
        if data and method not in ('POST', 'PUT'):
            raise BadRequest("%s requests cannot contain data" % method)

        # merge base headers and supplied headers
        headers = self.base_headers.update(headers)

        # encode data if needed
        if data and type(data) != str:
            data = json_dumps(data)
            headers['Content-type'] = "application/json"
        
        # don't a type when there is no content
        if not data:
            del headers['Content-type']
        
        # append url arguments if given
        if args:
            path = path + '?' + urlencode(args)
        
        # this is how we make a request
        def make_request():
            self.client.request(method, path, data, headers)
            return self.client.getresponse()
        
        try:
            # first try...
            response = make_request()
        except (socket.error, IOError, HTTPException):
            # maybe we just lost the socket, try again
            self._setup()
            response = make_request()
        
        # maybe we need to authenticate again
        if response.status == 401:
            self._authenticate()
            response = make_request()
        
        return response
    
    def get(self, path, data=None, headers=None, args=None):
        """
        """
        r = self.request('GET', path, data, headers, args)
        
        if r.status < 200 or r.status > 299:
            # TODO : this is probably throwing away some error information
            r.read()
            raise errors.ResponseError(r.status, r.reason)
        
        read_output = r.read()
        
        if r.getheader('content-type', 'text/plain') == "application/json":
            return json_loads(read_output)
        else:
            return read_output


class BadRequest(Exception):
    pass
