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
        
        for k in self.items:
            try:
                if k in ('updated', 'created'):
                    try:
                        setattr(self, k, datetime.strptime(kwargs[k], "%Y-%m-%dT%H:%M:%SZ"))
                        continue
                    except ValueError: pass
                
                setattr(self, k, kwargs[k])
            except KeyError, e:
                # TODO : proper exception
                raise Exception("%s must be specified when creating %s objects" %
                    (k, self.__class__.__name__))
    
    @property
    def model(self):
        """The API model name that this class represents
        """
        raise NotImplementedError("This method must be overriden by the super-class.")

    @property
    def items(self):
        """these are the keys of the things from the api we store
        """
        raise NotImplementedError("This method must be overriden by the super-class.")

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
