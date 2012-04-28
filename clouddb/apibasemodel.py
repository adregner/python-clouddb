# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
base model module

This code is licensed under the BSD license.  See COPYING for more details.
"""

import os

class APIBaseModel(object):
    """
    Instances of sub-classes of this class will inherit its easy property
    management capabilities.
    """
    
    def __init__(self, **kwargs):
        """
        """
        for k in self.items:
            try:
                setattr(self, k, kwargs[k])
            except KeyError, e:
                # TODO : proper exception
                raise Exception("%s must be specified when creating %s objects" %
                    (k, self.__class__.__name__))
    
    @property
    def items(self):
        """these are the keys of the things from the api we store
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
    
    def __getitem__(self, k):
        return getattr(self, k)
