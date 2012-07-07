# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb instance module

This code is licensed under the MIT license.  See COPYING for more details.
"""

import re

from clouddb.apibasemodel import APIBaseModel
from clouddb.models import *
import clouddb
import clouddb.helpers as helpers

class Instance(APIBaseModel):
    """
    Instances of this class represent an Instance in the Cloud Database service.
    This is simular to a MySQL environment within whitch you can have multiple
    databases.
    """
    
    def __init__(self, **kwargs):
        """
        Not to be called directaly.  These instances will be created by the 
        Connection class when you create or list the current instances.
        """
        APIBaseModel.__init__(self, **kwargs)
        self.flavor = Flavor(self.parent, **self.flavor)

    @property
    def model(self):
        return "instance"

    @property
    def items(self):
        return ('id', 'status', 'links', 'name', 'volume', 'flavor')

    @property
    def extended_items(self):
        return ('updated', 'created', 'hostname')

    def databases(self):
        """
        """
        apiout = self.client.get(self.path+'/databases')
        return helpers.build_from_list(self, Database, apiout['databases'])

    def users(self):
        """
        """
        apiout = self.client.get(self.path+'/users')
        return helpers.build_from_list(self, clouddb.models.user.User, apiout['users'])

    def get_database(self, database_id):
        """
        """
        return helpers.get_from_id(self, Database, database_id)

    def get_user(self, user_id):
        """
        """
        return helpers.get_from_id(self, User, user_id)

    def create_database(self, name, character_set=None, collate=None):
        """TODO : support creating multiple databases at once
        """
        # invalid database names
        if re.search('["\'`;,\\/]|^[@?# ]|[@?# ]$', name) or len(name) > 64:
            # TODO : proper error
            raise Exception()

        database = { 'name': str(name) }

        if character_set: database['character_set'] = character_set
        if collate: database['collate'] = collate

        self.client.post(self.path+'/databases', {'databases': [database]})
        return True

    def create_user(self, name, password, database=None):
        """TODO : support creating multiple users and databases at once
        """
        user = {'name': name, 'password': password}

        # TODO : check arguments for character and length restrictions
        if database is not None:
            user['databases'] = [{'name': database}]

        self.client.post(self.path+'/users', {'users': [user]})
        return True

    def enable_root(self):
        """Enable root access and return the root user's password
        """
        return self.client.post(self.path+'/root')['user']['password']

    def got_root(self):
        """Returns True if root access has been enabled on this database instance,
        and false otherwise.
        """
        return self.client.get(self.path+'/root')['rootEnabled']

    def restart(self):
        """Reboots the underlying virtual server powering this instance.
        """
        self.client.post(self.path+'/action', { 'restart': {} })
        return True

    def resize(self, flavor):
        """
        Change the "flavor" of the Rackspace Cloud Databases instance.  At presetnt
        mainly just means the RAM allocated to the instance.
        """
        # ram size of the instance
        if type(flavor) == Flavor:
            flavor = flavor.bookmark_link
        elif type(flavor) == dict:
            flavor = self.parent.flavors().find(**flavor)
        elif type(flavor) in (int, str, unicode):
            flavor = str(flavor)
        else:
            # TODO : proper error
            raise Exception()

        self.client.post(self.path+'/action', { 'resize': {'flavorRef': flavor} })
        return True

    def grow(self, size):
        """
        Resize the data storage volume of this instance.
        
        Note that it is impossiable to shrink the data storage volume of a Rackspace
        Cloud Databases instance, so size should be larger then the current size.
        """
        # size of the instance
        if size is not None and (type(size) == int or size.isdigit()):
            size = { 'size': str(size) }
        else:
            # TODO : proper error
            raise Exception()

        self.client.post(self.path+'/action', { 'resize': {'volume': size} })
        return True

    def delete(self):
        """Deletes this instance and all the databases and users within it.
        """
        self.client.delete(self.path)
        return True
