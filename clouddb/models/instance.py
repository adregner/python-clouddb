# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb instance module

This code is licensed under the MIT license.  See COPYING for more details.
"""

import re

from clouddb.models.base import APIBaseModel
from clouddb.models import *
from clouddb import helpers
from clouddb import consts
from clouddb import errors

class Instance(APIBaseModel):
    """
    Instances of this class represent an Instance in the Cloud Database service.
    This is simular to a MySQL environment within whitch you can have multiple
    databases.
    """
    
    model = "instance"
    
    items = ('id', 'status', 'links', 'name', 'volume', 'flavor')
    
    extended_items = ('updated', 'created', 'hostname')
    
    def __init__(self, **kwargs):
        """
        Not to be called directaly.  These instances will be created by the 
        Connection class when you create or list the current instances.
        """
        APIBaseModel.__init__(self, **kwargs)
        self.flavor = Flavor(**self.flavor)

    def databases(self):
        """
        """
        apiout = self.client.get(self.path+'/databases')
        return helpers.build_from_list(self, Database, apiout['databases'])

    def users(self):
        """
        """
        apiout = self.client.get(self.path+'/users')
        return helpers.build_from_list(self, User, apiout['users'])

    def get_database(self, database_id):
        """
        """
        return helpers.get_from_id(self, Database, database_id)

    def get_user(self, user_id):
        """
        """
        return helpers.get_from_id(self, User, user_id)

    def create_database(self, name, character_set=None, collate=None):
        """
        """
        databases = helpers.form_database_args(name, character_set, collate)
        self.client.post(self.path+'/databases', {'databases': databases})
        return True

    def create_user(self, name, password, databases=None, character_set=None, collate=None):
        """TODO : support creating multiple users
        """
        data = {'users': [{'name': name, 'password': password}]}

        if databases is not None:
            data['databases'] = helpers.form_database_args(databases, character_set, collate)
        
        self.client.post(self.path+'/users', data)
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
        """Change the "flavor" of the Rackspace Cloud Databases instance.  At presetnt
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
        """Resize the data storage volume of this instance.
        
        Note that it is impossiable to shrink the data storage volume of a Rackspace
        Cloud Databases instance, so size should be larger then the current size.
        """
        # size of the instance
        if size is not None and (type(size) == int or size.isdigit()):
            size = { 'size': int(size) }
        else:
            # TODO : proper error
            raise Exception()

        if self.size > size['size']:
            # TODO : proper error
            raise Exception("This instance has a data storage volume of %d GB and cannot " + \
                "be shrunk. (Tried to specify %d GB as new size.)" % (self.size, size['size']))

        self.client.post(self.path+'/action', { 'resize': {'volume': size} })
        return True

    def delete(self, wait=False):
        """Deletes this instance and all the databases and users within it."""
        
        self.client.delete(self.path)
        
        if wait is not False:
            wait = consts.delete_instance_wait_timeout if type(wait) == bool else float(wait)
            try:
                apiresult = helpers.poll_for_result(self,
                    self.path, "DELETED", #will never be this status...
                    wait,
                    consts.delete_instance_first_poll,
                    consts.delete_instance_poll_interval
                )
            except errors.RemoteResponseError as ex:
                # expected when we delete something
                if ex.status != 404:
                    raise ex
        
        return True

    def _sanatize_database_name(self, dbname):
        if not re.search('^[A-Z0-9_][A-Z0-9@\\?#_ ]*?[A-Z0-9_]?$', dbname, re.I) or len(dbname) > 64:
            # TODO : proper exception
            raise Exception("Database name '%s' contains invalid or too many characters" % dbname)
        return True

    def __str__(self):
        return APIBaseModel.__str__(self, ('id', 'name', 'volume', 'flavor'))