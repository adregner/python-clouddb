# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb database module

This code is licensed under the BSD license.  See COPYING for more details.
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
        self.our_path = "/instances/%s/%ss/%s" % (self.instance_id, self.model, self.name)

    @property
    def model(self):
        """
        """
        return "flavor"

    @property
    def items(self):
        """these are the keys of the things from the api we store
        """
        return ('name',)

    def delete(self):
        """Deletes this database
        """
        self.client.delete(self.our_path)
        return True
