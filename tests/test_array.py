"""Test case for schema generator for array type."""
import unittest
from unittest import mock
from ddt import ddt, data
from marshmallow import fields
from nadia.array import ArrayBuilder
from nadia.builder_mapping import BuilderMapping
from nadia import primitives


@ddt
class TestArrayBuilder(unittest.TestCase):
    """Test case for ArrayBuilder."""

    def test_return_type(self):
        """Building schema with ArrayBuilder should return marshmallow.fields.List instance."""
        mapping = BuilderMapping({'number': primitives.FloatBuilder})
        arr_def = {'type': 'array', 'items': {'type': 'number'}}
        builder = ArrayBuilder(mapping)
        self.assertEqual(fields.List, type(builder.build_schema(arr_def)))

    @data(primitives.FloatBuilder, primitives.IntegerBuilder, primitives.StringBuilder)
    def test_primitives_array(self, primitive_builder):
        """Building schema for array of primitives should return List with correct container."""
        mapping = BuilderMapping({primitive_builder.key: primitive_builder})
        arr_def = {'type': 'array', 'items': {'type': primitive_builder.key}}
        builder = ArrayBuilder(mapping)
        schema = builder.build_schema(arr_def)
        self.assertEqual(type(schema.container), primitive_builder.marshmallow_class)

    def test_nullable(self):
        """Building schema for array type should correctly use nullable field."""
        mapping = BuilderMapping({'number': primitives.FloatBuilder})
        arr_def = {'type': 'array', 'items': {'type': 'number'}}
        builder = ArrayBuilder(mapping)
        for nullable in (True, False):
            arr_def['nullable'] = nullable
            schema = builder.build_schema(arr_def)
            self.assertEqual(nullable, schema.allow_none)

    def test_required(self):
        """Building schema for array type should correctly utilize rquired field."""
        mapping = BuilderMapping({'number': primitives.FloatBuilder})
        arr_def = {'type': 'array', 'items': {'type': 'number'}}
        builder = ArrayBuilder(mapping)
        for required in (True, False):
            schema = builder.build_schema(arr_def, required=required)
            self.assertEqual(required, schema.required)
