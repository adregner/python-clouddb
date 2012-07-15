# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb flavor module

This code is licensed under the MIT license.  See COPYING for more details.
"""

from clouddb.models.base import APIBaseModel

class Flavor(APIBaseModel):
    """
    Instances of this class represent a flavor of a database instance in the
    Cloud Databases service.
    """
    
    model = "flavor"
    
    items = ('id', 'links')
    
    extended_items = ('name', 'ram')
    
    def __init__(self, **kwargs):
        """
        Not to be called directaly.  These instances will be created by the
        Connection class when you create or list the avaliable flavors.
        """
        APIBaseModel.__init__(self, **kwargs)

    def __str__(self):
        return APIBaseModel.__str__(self, ('id', 'name', 'ram'))
