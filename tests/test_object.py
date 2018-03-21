"""Test cases for schema generator for object type."""
import unittest
from unittest import mock
from ddt import ddt, data
from marshmallow import fields, Schema
from nadia.object import ObjectBuilder
from nadia.common import Builder
from nadia.builder_provider import BuilderProvider
from nadia import primitives


@ddt
class TestObjectBuilder(unittest.TestCase):
    """Test case for ObjectBuilder."""

    provider = None
    properties = None
    required = None

    def setUp(self):
        number_mock = mock.Mock()
        number_mock.build_schema.return_value = fields.Float()
        int_mock = mock.Mock()
        int_mock.build_schema.return_value = fields.Int()
        str_mock = mock.Mock()
        str_mock.build_schema.return_value = fields.Str()
        self.provider = BuilderProvider({'number': number_mock, 'integer': int_mock,
                                         'string': str_mock})
        self.properties = {'x': {'type': 'number'},
                           'y': {'type': 'integer'},
                           'name': {'type': 'string'}}
        self.required = ['x', 'y']

    def test_return_type(self):
        """Building schema with ObjectBuilder should return marshmallow.fields.Nested instance."""
        provider = BuilderProvider({'number': mock.Mock(spec=Builder)})
        obj_def = {'type': 'object', 'properties': {'num1': {'type': 'number'}}}
        builder = ObjectBuilder(provider)
        self.assertEqual(fields.Nested, type(builder.build_schema(obj_def)))

    def test_nullable(self):
        """Building schema for object type should correctly use nullable field."""
        obj_def = {'type': 'object', 'properties': self.properties}
        builder = ObjectBuilder(self.provider)
        for nullable in (True, False):
            obj_def['nullable'] = nullable
            self.assertEqual(nullable, builder.build_schema(obj_def).allow_none)

    def test_required(self):
        """Building schema for object type should correctly use required field."""
        obj_def = {'type': 'object', 'properties': self.properties}
        builder = ObjectBuilder(self.provider)
        for required in (True, False):
            self.assertEqual(required, builder.build_schema(obj_def, required=required).required)

    def test_properties_building(self):
        """Constructing nested objects attributes should correctly call provided schema builders."""
        obj_def = {'type': 'object', 'properties': self.properties}
        builder = ObjectBuilder(self.provider)
        props_schemas = builder.construct_attributes_schemas(obj_def)
        for prop_name, prop in self.properties.items():
            prop_builder = self.provider.get_builder(prop['type'])
            prop_builder.build_schema.assert_called_once()
            self.assertEqual(props_schemas[prop_name], prop_builder.build_schema.return_value)

    @mock.patch('nadia.object.fields.Nested')
    @mock.patch('nadia.object.ObjectBuilder.create_schema_type')
    @mock.patch('nadia.object.ObjectBuilder.construct_attributes_schemas')
    def test_build_schema(self, cas, cst, nested):
        """Constructing object schema should result in correct call chain."""
        obj_def = {'type': 'object', 'properties': self.properties}
        builder = ObjectBuilder(self.provider)
        schema = builder.build_schema(obj_def)
        cas.assert_called_once_with(obj_def)
        cst.assert_called_once_with(cas.return_value)
        nested.assert_called_once_with(cst.return_value, allow_none=False, required=False)
