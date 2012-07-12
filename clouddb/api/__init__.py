# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
This is an attempt to abstract away some of the functionality that allows a
python library to interface with a RESTful API via HTTP.
"""

from clouddb.api.requester import APIRequester

__all__ = ('APIRequester', )
