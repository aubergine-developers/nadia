nadia Tutorial
==============


Basic concepts
--------------

The basic workflow with **nadia** consists of the following steps:

1. Load your yaml or json specification file.
2. Construct SchemaBuilder - **nadia** defines convenient method for creating the reasonable
   one via factory :py:meth:`nadia.api.SchemaBuilder.create`
3. Extract object definitions for which you want to create schema from the loaded dictionary.
4. Construct schema for the extracted object. Note that the schema will contain top level `content`
   field.
5. Use your schema to validate or serialize/deserialize objects.

Why do all schemas created by **nadia** have a top level `content` field?
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
The reason why nadia hides your real object in the `content` field is that
not all OpenAPI schemas can be expressed as :py:class:`marshmallow.Schema`.
For instance, consider the following schema:

.. code-block:: yml

   type: array
   items:
     type: number

Such a data type can be modelled as :py:class:`marshmallow.field.List` but not as
a `Schema`. However, if you wrap it inside a larger object under `content` field, than a Schema
for such object can be constructed. This step is done automatically by **nadia** - even if it is
unneccesary, to make behaviour consistent for all objects.


Creating Schemabuilders
-----------------------
You can create a :py:class:`nadia.api.SchemaBuilder` instance in one of two ways:

1. You can explicitly initialize it by passing a object providings component builders (see :py:mod:`nadia.builder_provider`.
2. You can use :py:class:`nadia.api.SchemaBuilder.create` staticmethod to construct default builder using **nadia's** default builder providers.
