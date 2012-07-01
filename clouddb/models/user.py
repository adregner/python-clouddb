# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb user module

This code is licensed under the MIT license.  See COPYING for more details.
"""

from clouddb.apibasemodel import APIBaseModel

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
        
        for db_n in xrange(len(self.databases)):
            self.databases[n] = Database(self.parent, **self.databases[n])
        
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
        return ('name', 'databases')

    def delete(self):
        """Deletes this user
        """
        self.client.delete(self.our_path)
        return True
