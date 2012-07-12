# -*- encoding: utf-8 -*-
__author__ = "Andrew Regner <andrew@aregner.com>"

"""
clouddb models module

This module imports all the model classes at once for your convience.

This code is licensed under the MIT license.  See COPYING for more details.
"""

from clouddb.models.database import Database
from clouddb.models.flavor import Flavor
from clouddb.models.instance import Instance
from clouddb.models.user import User

__all__ = ('Database', 'Flavor', 'Instance', 'User')
