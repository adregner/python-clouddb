# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb flavor module

This code is licensed under the BSD license.  See COPYING for more details.
"""

import os

from clouddb.apibasemodel import APIBaseModel

class Flavor(APIBaseModel):
    """
    Instances of this class represent a flavor of a database instance in the
    Cloud Databases service.
    """
    
    def __init__(self, **kwargs):
        """
        Not to be called directaly.  These instances will be created by the
        Connection class when you create or list the avaliable flavors.
        """
        APIBaseModel.__init__(self, **kwargs)

    @property
    def items(self):
        """these are the keys of the things from the api we store
        """
        return ('id', 'links', 'name')

    def __getattr__(self, k):
        """
        """
        if k in ('self_link', 'bookmark_link'):
            k = k.split('_')[0]
            for link in self.links:
                if link['rel'] == k:
                    return link['href']
        return self.__dict__[k]

    def __str__(self):
        """
        """
        return APIBaseModel.__str__(self, ('id', 'name', 'self_link', 'bookmark_link'))
