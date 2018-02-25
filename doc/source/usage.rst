Basic usage
===========

We will ilustrate nadia's usage on the usual `OpenAPI petstore example <https://github.com/OAI/OpenAPI-Specification/blob/master/examples/v3.0/petstore.yaml>`_. Assuming you have the file save in your current directory, the following snippet should:
1. Load the speficication.
2. Create schema builder.
3. Build schema for Pet object.
4. Validate two sample objects using the given schema.

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
