# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

""" This code is licensed under the MIT license.  See COPYING for more details. """

import os

from clouddb.models import *

def build_from_list(self, klass, items):
    """
    """
    results = list()
    for i in items:
        results.append(klass(parent = self, **i))
    return APIListHelper(results)

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
    return klass(parent = self, **apiout[kname])

class APIListHelper(object):
    """
    This class represents a list of common objects.  It providers an iterator and list
    interface, as well as helper methods to return an element based on an arbitrary key.
    """

    def __init__(self, items):
        """
        """
        self.items = items

        if len(self) > 0:
            self.klass = items[0]
            self.key_field = items[0].items[0]

    def find(self, key=None, **query):
        """
        """
        # let a string of a number still be a number
        if key and type(key) == str and key.isdigit():
            key = int(key)

        # check for a simple thing to match
        if key:
            for item in self:
                if item[self.key_field] == key:
                    return item

        # doing it the harder way
        results = []
        for item in self:
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

    def __iter__(self):
        self.iter_i = -1
        return self

    def next(self):
        self.iter_i += 1
        try:
            return self.items[self.iter_i]
        except IndexError:
            raise StopIteration

    def __getitem__(self, n):
        return self.items[n]

    def __getslice__(self, i, j):
        return self.items[i:j]

    def __setitem__(self, n, value):
        self.items[n] = value

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return '[' + ', '.join([str(i) for i in self.items]) + ']'

