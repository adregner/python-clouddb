#!/usr/bin/env python -t3
# -*- coding: utf-8 -*-

# Copyright (C) 2011 by Andrew Regner <andrew@aregner.com>

import os
from distutils.core import setup

from clouddb import consts

setup_params = {}
setup_params['name'] = "clouddb"
setup_params['version'] = consts.__version__
setup_params['description'] = "Python object oriended model-based interface to the Rackspace Cloud Databases API."
setup_params["long_description"] = "".join([
        "",
        ])
setup_params['author'] = "Andrew Regner"
setup_params['author_email'] = "andrew@aregner.com"
setup_params['url'] = "http://adregner.github.com/python-clouddb/"
setup_params['license'] = "MIT"
#setup_params['scripts'] = [
#        "",
#        ]
setup_params['packages'] = [
        "clouddb",
        "clouddb.api",
        "clouddb.models",
        ]
setup_params['data_files'] = [
        ("share/doc/python-%s" % setup_params['name'], [
            "COPYING",
            "README",
            ]),
        ]
#setup_params['requires'] = [
#        "",
#        ]

# make a link to the readme file so we can pretend it is normal
if not os.path.isfile("README"):
    os.link("README.md", "README")

setup(**setup_params)
