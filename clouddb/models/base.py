# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
base model module

This code is licensed under the MIT license.  See COPYING for more details.
"""

import os
from datetime import datetime

from clouddb.api.requester import APIRequester

class APIBaseModel(object):
    """
    Instances of sub-classes of this class will inherit its easy property
    management capabilities.
    """
    
    model = None
    
    items = None
    
    extended_items = ()
    
    def __init__(self, **kwargs):
        """
        """
        self.client = APIRequester
        
        self._data = {}
        
        self._load_into_self(kwargs, self.items)
    
    def _load_into_self(self, new_data, keys):
        """
        """
        try:
            d = dict([ (k, new_data[k]) for k in keys ])
        except KeyError:
            # TODO : proper exception
            raise Exception("%s must be specified when using %s objects" %
                (k, self.__class__.__name__))
        
        for time_key in ('updated', 'created'):
            if time_key in d:
                d[time_key] = datetime.strptime(d[time_key], "%Y-%m-%dT%H:%M:%S")
        
        if 'links' in d:
            for link_key in ('self_link', 'bookmark_link'):
                k = link_key.split('_')[0]
                for l in d['links']:
                    if l['rel'] == k:
                        d[link_key] = l['href']
        
        if 'volume' in d:
            d['size'] = d['volume']['size']
        
        self._data.update(d)

    @property
    def path(self):
        """The API path to this item... default implementation is just a guess."""
        return self.path_to(self._data['id'] if 'id' in self._data else self._data['name'])

    @classmethod
    def path_to(self, theid):
        """Constructs a path within the API to an item like this."""
        return "/%ss/%s" % (self.model, str(theid))

    @classmethod
    def find(cls, key=None, **query):
        """Finds an item of the given model based on a key or specific parameters.

        key :: The unique identifier for this specific model.  Will return an instance
        of that model with that specific name or id.
        
        query :: arbitrary name=value pairs that will be matched agains a list of
        all the avaliable items of this model.  If there are no matches, None will
        be returned.  If there is one match, only that single model is returned.  If
        there are multiple matches, a list of those models will be returned.
        """
        # get just this item
        if key:
            obj_data = APIRequester.get(cls.path_to(key))[cls.model]
            return cls.__new__(**obj_data)

        # look at all the items
        else:
            objects = [ cls(**obj_data) for obj_data in
                APIRequester.get("/%ss" % cls.model)["%ss" % cls.model] ]

            # doing it the harder way
            results = []
            for item in objects:
                addit = True
                for k in query.keys():
                    if query[k] != item[k]:
                        addit = False
                if addit:
                    results.append(item)

            # check if we have a single match, and return intelligently
            if len(results) == 0:
                return None
            elif len(results) == 1:
                return results[0]
            else:
                return results

    def __str__(self, info_items=None):
        if info_items is None:
            info_items = self._data.keys().remove('links')
        fq_name = "%s.%s" % (self.__module__, self.__class__.__name__)
        props = ", ".join([ "%s='%s'" % (k, self[k]) for k in info_items ])
        return "<%s %s>" % (fq_name, props)

    def __getattr__(self, k):
        try:
            return self._get_model_property(k)
        except KeyError:
            raise AttributeError(k)

    def __getitem__(self, k):
        return self._get_model_property(k)

    def _get_model_property(self, k):
        """Gets a property from ourself, and requests more data from the API if its not there yet."""
        if k in self.extended_items and k not in self._data:
            moar_data = self.client.get(self.path)
            self._load_into_self(moar_data[self.model], self.extended_items)
        
        return self._data[k]
