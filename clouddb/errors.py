# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
exception classes

This code is licensed under the MIT license.  See COPYING for more details.
"""

class APIError(StandardError):
    """Base class for all errors and exceptions."""
    pass

class RemoteResponseError(APIError):
    """Raised when the remote service returns an error."""
    def __init__(self, status, reason):
        self.status = status
        self.reason = reason
        Exception.__init__(self)

    def __str__(self):
        return '%d: %s' % (self.status, self.reason)

    def __repr__(self):
        return '%d: %s' % (self.status, self.reason)

class BadRequest(APIError):
    pass
