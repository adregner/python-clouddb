# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb flavor module

This code is licensed under the MIT license.  See COPYING for more details.
"""

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
        
        self.our_path = "/%ss/%s" % (self.model, self.id)

    @property
    def model(self):
        """
        """
        return "flavor"

    @property
    def items(self):
        """these are the keys of the things from the api we store
        """
        return ('id', 'links', 'name', 'ram', 'vcpus')

    def __str__(self):
        """
        """
        return APIBaseModel.__str__(self, ('id', 'name', 'self_link', 'bookmark_link'))
