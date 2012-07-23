# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb user module

This code is licensed under the MIT license.  See COPYING for more details.
"""

from clouddb.models.base import APIBaseModel
from clouddb.models import Database

class User(APIBaseModel):
    """
    Instances of this class represent a user in the Cloud Database API.
    """

    model = "user"

    items = ('name', 'databases')

    extended_items = ()

    def __init__(self, parent, **kwargs):
        """
        Sets the initial details for a user in the API.  Instances of this class
        will be created by the Database class when accessing the users on a 
        database.  You do not need to create instances of this class yourself.
        """
        APIBaseModel.__init__(self, **kwargs)

        self.parent = parent
        self.instance_id = self.parent.id

        self.databases = [ Database(parent = self.parent, **dbase)
            for dbase in self.databases ]

    @property
    def path(self):
        return "/instances/%s/%ss/%s" % (self.instance_id, self.model, self.name)

    @classmethod
    def find(cls, key=None, **query):
        """This method is not supported on this class at this time."""
        raise NotImplementedError("This method is not yet supported on this model.")

    def delete(self):
        """Deletes this user."""
        self.client.delete(self.path)
        return True
