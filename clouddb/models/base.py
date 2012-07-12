# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
base model module

This code is licensed under the MIT license.  See COPYING for more details.
"""

import os
from datetime import datetime

class APIBaseModel(object):
    """
    Instances of sub-classes of this class will inherit its easy property
    management capabilities.
    """
    
    def __init__(self, parent, **kwargs):
        """
        """
        self.parent = parent
        self.client = parent.client
        
        self._data = {}
        
        self._load_into_self(kwargs, self.items)
    
    def _load_into_self(self, new_data, keys):
        """
        """
        try:
            d = dict([ (k, new_data[k]) for k in keys ])
        except KeyError as e:
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
        
        self._data.update(d)
    
    @property
    def model(self):
        """The API model name that this class represents
        """
        raise NotImplementedError("This method must be overriden by the super-class.")

    @property
    def path(self):
        """The API path to this item... default implementation is just a guess
        """
        return "/%ss/%s" % (self.model, self._data['id'] if 'id' in self._data else self['name'])

    @property
    def items(self):
        """these are the keys of the things from the api we store
        """
        raise NotImplementedError("This method must be overriden by the super-class.")

    @property
    def extended_items(self):
        """these are the keys of things that are in this model, but require an
        additional API call to retrieve
        """
        return ()

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
        if k in self.extended_items and k not in self._data:
            moar_data = self.client.get(self.path)
            self._load_into_self(moar_data[self.model], self.extended_items)
        
        return self._data[k]
