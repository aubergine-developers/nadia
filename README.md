# nadia: create marshmallow Schemas OpenAPI 3 objects.

[![Build Status](https://travis-ci.org/aubergine-developers/nadia.svg?branch=master)](https://travis-ci.org/aubergine-developers/nadia)
[![Documentation Status](https://readthedocs.org/projects/nadia/badge/?version=latest)](http://nadia.readthedocs.io/en/latest/?badge=latest)
  

**nadia** is a small and lightweight library for creating marshmallow Schemas from schemas defined in your OpenAPI spec.

## Basic usage

```python

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
```

## Feature overview
Currently **nadia** supports all of the OpenAPI 3 data types, except allOf/anyOf fields. Most of the options like required, nullable, etc. are also supported.