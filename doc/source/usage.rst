Basic usage
===========

nadia's usage is as simple as it gets. Suppose you have standard
`OpenAPI petstore example <https://github.com/OAI/OpenAPI-Specification/blob/master/examples/v3.0/petstore.yaml>`_ yaml saved in your current directory. Below short snippet will create Schema for the pet object and use it to validate two example objects.

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
