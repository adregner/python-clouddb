# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

""" This code is licensed under the MIT license.  See COPYING for more details. """

import time
import os

from clouddb.models import *
from clouddb import errors
from clouddb import consts

def build_from_list(self, klass, items):
    """
    """
    results = list()
    for i in items:
        results.append(klass(parent = self, **i))
    return results

def get_from_id(self, klass, the_id):
    """
    """
    kname = klass.__name__.lower()
    try:
        the_id = int(the_id)
    except ValueError:
        # TODO : proper exception class
        raise Exception("%s_id must be an integer" % kname)
    
    apiout = self.client.get('/%s/%d' % (kname, the_id))
    return klass(**apiout[kname])

def poll_for_result(self, path, status, timeout, first_poll, poll_interval):
    """
    """
    # calculate when we are going to bail
    drop_dead = time.time() + timeout
    
    # wait at least this long
    time.sleep(first_poll)
    
    # check the status
    apiresult = self.client.get(path)
    
    # these are the things we need to know
    model = apiresult.keys()[0].title()
    apiresult = apiresult.values()[0]
    new_id = apiresult["id"]
    
    # check if it's "ready"
    while apiresult['status'] != status:
        if time.time() >= drop_dead:
            # TODO : proper error
            raise Exception("%(model)s timeout error.  New %(model)s id = %(id)s"
                % {'model':model, 'id':new_id})
            # or should this just return the instance?
            #return Instance(**apiresult['instance'])
        else:
            time.sleep(poll_interval)
        apiresult = self.client.get(path).values()[0]
    
    return apiresult

def maybe_wait_until_deleted(self, wait, path):
    """
    """
    if wait is not False:
        wait = consts.delete_instance_wait_timeout if type(wait) == bool else float(wait)
        try:
            apiresult = helpers.poll_for_result(self,
                path, "DELETED", #will never be this status...
                wait,
                consts.delete_instance_first_poll,
                consts.delete_instance_poll_interval
            )
        except errors.RemoteResponseError as ex:
            # expected when we delete something
            if ex.status != 404:
                raise ex
    

def form_database_args(self, name, character_set, collate):
    """Takes many different forms of arguments and creates a list that the API
    will like to represent a database or databases.
    """
    if type(name) == dict:
        databases = [databases]
    elif type(name) in (list, tuple) and len(name) >= 1 and type(name[0]) == dict:
        databases = list(name)
    elif type(name) in (list, tuple) and len(name) >= 1 and type(name[0]) in (str, unicode):
        databases = [{'name': dbname, 'character_set': character_set, 'collate': collate} for dbname in name]
    elif type(name) in (str, unicode):
        databases = [{'name': str(name), 'character_set': character_set, 'collate': collate}]
    
    for n in xrange(len(databases)):
        self._sanatize_database_name(databases[n]['name'])
        if 'collate' in databases[n] and databases[n]['collate'] is None:
            del databases[n]['collate']
        elif 'character_set' in databases[n] and databases[n]['character_set'] is None:
            del databases[n]['character_set']
    
    return databases
