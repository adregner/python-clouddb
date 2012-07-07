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
        
        self._load_into_self(kwargs, self.items)
    
    def _load_into_self(self, data, keys):
        """
        """
        for k in keys:
            try:
                if k in ('updated', 'created'):
                    try:
                        setattr(self, k, datetime.strptime(data[k], "%Y-%m-%dT%H:%M:%SZ"))
                        continue
                    except ValueError: pass
                
                setattr(self, k, data[k])
            except KeyError, e:
                # TODO : proper exception
                raise Exception("%s must be specified when using %s objects" %
                    (k, self.__class__.__name__))
    
    @property
    def model(self):
        """The API model name that this class represents
        """
        raise NotImplementedError("This method must be overriden by the super-class.")

    @property
    def path(self):
        """The API path to this item... default implementation is just a guess
        """
        return "/%ss/%s" % (self.model, self.id if 'id' in self else self.name)

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
        return tuple()

    def __str__(self, info_items=None):
        """
        """
        if info_items is None:
            info_items = self.items
        fq_name = "%s.%s" % (self.__module__, self.__class__.__name__)
        props = ", ".join([ "%s='%s'" % (k, self[k]) for k in info_items ])
        return "<%s %s>" % (fq_name, props)

    def __getattr__(self, k):
        """
        """
        if k in self.extended_items and k not in self:
            moar_data = self.client.get(self.path)
            self._load_into_self(moar_data[self.model], self.extended_items)
        if k in ('self_link', 'bookmark_link'):
            k = k.split('_')[0]
            for link in self.links:
                if link['rel'] == k:
                    return link['href']
        return self.__dict__[k]

    def __getitem__(self, k):
        return getattr(self, k)

    def __contains__(self, k):
        return k in self.__dict__
