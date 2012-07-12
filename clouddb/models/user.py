# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb user module

This code is licensed under the MIT license.  See COPYING for more details.
"""

from clouddb.models.base import APIBaseModel
from clouddb.helpers import APIListHelper

class User(APIBaseModel):
    """
    Instances of this class represent a user in the Cloud Database API.
    """
    
    def __init__(self, **kwargs):
        """
        Sets the initial details for a user in the API.  Instances of this class
        will be created by the Database class when accessing the users on a 
        database.  You do not need to create instances of this class yourself.
        """
        APIBaseModel.__init__(self, **kwargs)
        
        self.databases = APIListHelper( [ Database(parent = self.parent, **dbase)
            for dbase in self.databases ] )
        
        self.instance_id = self.parent.id

    @property
    def model(self):
        return "flavor"

    @property
    def path(self):
        return "/instances/%s/%ss/%s" % (self.instance_id, self.model, self.name)

    @property
    def items(self):
        return ('name', 'databases')

    def delete(self):
        """Deletes this user
        """
        self.client.delete(self.path)
        return True
