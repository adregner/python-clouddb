python-clouddb
==============

Python bindings to the Rackspace Cloud Databases API.

This library aims to implement the full capability of the API, and extend it in places where we can provide better and more intelligent functionality without sacrificing any robustness of available options.

To get it up and going, just do this in your Python script(s):

```python
import clouddb
raxdb = clouddb.Connection("myCloudUsername", "somereallylongapikey", region="ord")

for instance in raxdb.instances():
    print "%s (%d MB) : %s" % (instance.name, instance.flavor.ram, instance.hostnmae)
```

At the time of this writing, there are two available regions, "DFW" and "ORD", located in Rackspace's Dallas, TX and Chicago, IL data centers respectively.  When the optional "auth_url" parameter is passed, you can change the environment the library authenticates with, such as setting it to the value of "clouddb.consts.uk_authurl" to authenticate with a Rackspace Cloud account based in the United Kingdom, and have access to the London, England data center.  (region="LON").

The API operates around four principal models, an instance (a virtual server running a MySQL daemon), a database, a user, and a flavor (RAM size and configuration of the instance).  For more information on the API itself, consult the [Rackspace Cloud Databases API guide] (http://docs.rackspace.com/cdb/api/v1.0/cdb-devguide/content/index.html).

As show in the example above, you can get a list of your database instances off of the Connection object.  You can also create a new Instance through that object, as well as get a list of the available Flavors.

The Instance object lets you see the databases and users it contains, and manage both.  It also contains methods to restart, resize, enable root access and delete the instance.  The User and Database objects contain methods to manage themselves and delete either.

Everything is intended to be set up pretty self-explanatory and logical, but please feel free to make suggestions or patches for things that could be better.
