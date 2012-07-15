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
    return klass(parent = self, **apiout[kname])
