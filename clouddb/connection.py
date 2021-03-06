# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb connection module

This is your starting point for accessing the Cloud Database service.

This code is licensed under the MIT license.  See COPYING for more details.
"""

from clouddb.api import APIRequester
from clouddb.models import *
import clouddb.consts as consts
import clouddb.helpers as helpers

class Connection(object):
    """
    Represents a connection, or an active session with the Cloud Database API.
    Use this class to create a connection to the service, and to get other
    objects that you can use to perform any required action with the service.
    """
    
    def __init__(self, username, api_key, region, auth_url=None, **kwargs):
        """
        Use this to create your connection to the service with your Rackspace
        Cloud user name and API key, and access the Cloud Databases service in
        the desired region where the service is avaliable. (ORD, DFW, LON).
        
        The auth_url parameter can be used to connect to another compatiable
        service endpoint other then Rackspace.
        """
        self.user = username
        self.key = api_key
        self.region = region.upper()
        
        if not auth_url:
            auth_url = consts.default_authurl
        
        self.debug = int(kwargs.get('debug', 0))
        
        self.client = APIRequester(self.user, self.key, 
            auth_url, "cloudDatabases", self.region, debug=self.debug)

    def __str__(self):
        """
        """
        fq_name = "%s.%s" % (self.__module__, self.__class__.__name__)
        return "<%s object, username=%s, region=%s>" % (fq_name, self.user, self.region)

    def info(self):
        """
        """
        # TODO : this doesn't work for some reason, but it's supposed to return
        # the api and contract version info
        return self.client.get('/')

    def instances(self):
        """
        """
        apiout = self.client.get('/instances')
        return helpers.build_from_list(self, Instance, apiout['instances'])

    def flavors(self):
        """
        """
        apiout = self.client.get('/flavors')
        return helpers.build_from_list(self, Flavor, apiout['flavors'])

    def get_flavor(self, flavor_id):
        """
        """
        return helpers.get_from_id(self, Flavor, flavor_id)

    def get_instance(self, instance_id):
        """untested
        """
        return helpers.get_from_id(self, Instance, instance_id)

    def create_instance(self, name=None, flavor=None, size=None, **instance):
        """Creates a new instance, optionally with a new database and user pre-made.
        
        Required parameters:
            name :: Arbitrary string representation for the new instance.
            
            flavor :: Flavor (int id, str href or Flavor object) of the instance to be made.
            
            size :: Size (in GB) of the database data storage volume.
        
        Optional parameters:
            databases :: Name of a new database to be created within the new instance.
            
            user :: User name of a user to be granted access to the new database above.
            
            wait :: Poll at regular intervals and return only once the instance 
            is finished building on the backend.
            
            instance :: Dictionary object that will be encoded and sent directaly
            in the request to the API.  See the README file that came with this
            package for information on its format.
        
        The API does support creating multiple databases and users at once along
        with a new instance, however this function does not yet have support for
        that.  Future versions will.
        
        example:
            # creates a new mysql instance, with 1GB of RAM and a 3 GB data storage volume
            instance = raxdb.create_instance("my-db-server", clouddb.Flavor(ram=1024), 3)
            
            # creates a new instance, with a 10GB data storage volume, 2GB of RAM (using the
            API's upstream ID for that particular flavor), 3 initial databases and one inital
            user.  TODO : see if that user is associated with any databases.
            instance = raxdb.create_instance("another-db-server", flavorRef="3", size=10,
                databases=["prod_db", "dev_db", "catpics"], users="chezburger")
        """
        # name
        if name is not None:
            instance['name'] = str(name)

        # ram size of the instance
        if type(flavor) == Flavor:
            instance['flavorRef'] = flavor.bookmark_link
        elif type(flavor) == dict:
            instance['flavorRef'] = Flavor.find(**flavor)
        elif type(flavor) in (int, str, unicode):
            instance['flavorRef'] = str(flavor)

        # size of the instance
        if size is not None and (type(size) == int or size.isdigit()):
            instance['volume'] = { 'size': int(size) }

        # check for required parameters
        for k in ('name', 'volume', 'flavorRef'):
            if k not in instance:
                # TODO : proper exception
                raise Exception("%s must be specified to create a new instance." % k)

        # initial database(s)
        if instance.get('databases', None) is not None:
            instance['databases'] = helpers.form_database_args(instance.get('databases'),
                instance.get('character_set', None), instance.get('collate', None))

        # initial user
        # TODO : we probably need to associate them with the aforementioned database(s)
        if type(instance.get('user', None)) == dict:
            instance['users'] = [instance.get('user')]
        elif type(instance.get('user', None)) in (str, unicode):
            instance['users'] = [{'name': str(instance.get('user'))}]
        if 'user' in instance:
            del instance['user']

        # this shouldn't be passed to the API
        wait = instance.get('wait', False)
        if wait: del instance['wait']

        apiresult = self.client.post('/instances', { 'instance': instance })

        # to wait or not to wait
        if wait is not False:
            wait = consts.create_instance_wait_timeout if type(wait) == bool else float(wait)
            apiresult = helpers.poll_for_result(self,
                Instance.path_to(apiresult['instance']['id']), "ACTIVE",
                wait,
                consts.create_instance_first_poll,
                consts.create_instance_poll_interval
            )
            return Instance(**apiresult)
            
        else:
            return Instance(**apiresult['instance'])

    def new_instance(self, **kwargs):
        """alias for create_instance
        """
        return self.create_instance(**kwargs)

    def delete_instance(self, instance_id, wait=False):
        """
        """
        # check to see if this is actually a name and not an ID
        if not (len(instance_id) == 36 and len(instance_id.replace('-', '')) == 32):
            instance = Instance.find(name=instance_id)
            if type(instance) == Instance:
                instance_id = instance.id
            else:
                # TODO : proper exception
                raise Exception("Error resolving %s to a single instance" % instance_id)
        
        self.client.delete(Instance.path_to(instance_id))
        helpers.maybe_wait_until_deleted(self, wait, Instance.path_to(instance_id))
        
        return True
