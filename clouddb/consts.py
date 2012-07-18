# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

""" This code is licensed under the MIT license.  See COPYING for more details. """

__version__ = "0.1"
user_agent = "python-clouddb/%s" % __version__
us_authurl = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
uk_authurl = 'https://lon.identity.api.rackspacecloud.com/v2.0/tokens'
default_authurl = us_authurl

# wait times and parameters used in clouddb.helpers.wait_for_result
create_instance_wait_timeout = 120.0
create_instance_first_poll = 45.0
create_instance_poll_interval = 7.0

delete_instance_wait_timeout = 40.0
delete_instance_first_poll = 5.0
delete_instance_poll_interval = 3.0
