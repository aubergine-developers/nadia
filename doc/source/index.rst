.. nadia documentation master file, created by
   sphinx-quickstart on Sat Feb 24 23:44:09 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

nadia documentation
=================================

**nadia** is a small and lightweight library for creating `marshmallow <https://marshmallow.readthedocs.io/en/latest/>`_ schemas for objects defined in OpeanAPI 3 specifications.

Usage example
-------------
**nadia** 's usage is as simple as it gets. Suppose you have standard
`OpenAPI petstore example <https://github.com/OAI/OpenAPI-Specification/blob/master/examples/v3.0/petstore.yaml>`_ yaml saved in your current directory. Below short snippet will create Schema for the Pet object and use it to validate two example objects.

.. code-block:: python

   import yaml
   import nadia.api

   with open('petstore.yaml') as petstore:
       data = yaml.load(petstore)

   builder = nadia.api.SchemaBuilder.create()
   schema = builder.build(data['components']['schemas']['Pet'])

   valid_pet = {'id': 100, 'name': 'Doggo', 'tag': 'sometag'}
   invalid_pet = {'id': 'foo', 'name': 'Lessie', 'tag': ['tag1', 'tag2']}

   print('Validation errors for Doggo: {}'.format(schema.validate({'content': valid_pet})))
   print('Validation errors for Lessie: {}'.format(schema.validate({'content': invalid_pet})))

What can **nadia** do?
----------------------
* construct Schema for your data type provided as a dict read from your spec's yml or json file.
* skip you the hassle of redesigning your Schema definitions everytime your specification changes. Just load your specs and let **nadia** do the job for you.

What can't **nadia** do?
------------------------
* use json references in your yaml/json file - you have to resolve them yourself.
* validate your OpenAPI specification - but there are tools that can do that for you.
* generate webserver using some xyz framework.

.. toctree::
   :caption: User documentation
   :maxdepth: 4

   userdoc/tutorial.rst

.. toctree::
   :caption: Technical reference
   :maxdepth: 4

   reference/nadia.rst
