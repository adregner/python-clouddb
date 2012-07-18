# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb database module

This code is licensed under the MIT license.  See COPYING for more details.
"""

from clouddb.models.base import APIBaseModel

class Database(APIBaseModel):
    """
    Instances of this class represent a database in the Cloud Database service.
    """
    
    model = "database"
    
    items = ('name',)
    
    extended_items = ()
    
    def __init__(self, parent, **kwargs):
        """
        Not to be called directaly.  These instances will be created by the 
        Connection class when you create or list your databases.
        """
        APIBaseModel.__init__(self, **kwargs)

        self.parent = parent
        self.instance_id = self.parent.id

    @property
    def path(self):
        return "/instances/%s/%ss/%s" % (self.instance_id, self.model, self.name)

    @classmethod
    def find(cls, key=None, **query):
        """This method is not supported on this class at this time."""
        raise NotImplementedError("This method is not yet supported on this model.")

    def delete(self):
        """Deletes this database."""
        self.client.delete(self.path)
        return True
