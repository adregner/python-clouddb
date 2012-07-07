# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb database module

This code is licensed under the MIT license.  See COPYING for more details.
"""

from clouddb.apibasemodel import APIBaseModel

class Database(APIBaseModel):
    """
    Instances of this class represent a database in the Cloud Database service.
    """
    
    def __init__(self, **kwargs):
        """
        Not to be called directaly.  These instances will be created by the 
        Connection class when you create or list your databases.
        """
        APIBaseModel.__init__(self, **kwargs)

        self.instance_id = self.parent.id

    @property
    def model(self):
        return "flavor"

    @property
    def path(self):
        return "/instances/%s/%ss/%s" % (self.instance_id, self.model, self.name)

    @property
    def items(self):
        return ('name',)

    def delete(self):
        """Deletes this database
        """
        self.client.delete(self.path)
        return True
