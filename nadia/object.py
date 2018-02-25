"""Implementation of validation builder for object type."""
from uuid import uuid4
from marshmallow import fields
from nadia.schema import NadiaSchema
from nadia.common import Builder


class ObjectBuilder(Builder):
    """Validator builder for array datatype."""

    def build_schema(self, spec_dict):
        """Build validator for custom object datatype."""
        attrs = self.construct_attributes_schemas(spec_dict['properties'])
        obj_schema = self.create_schema_type(attrs)
        return fields.Nested(obj_schema, **self.translate_args(spec_dict))

    def construct_attributes_schemas(self, properties):
        """Construct dictionary of schemas corresponding to object properties dict."""
        attr_schemas = {}
        for prop_name, prop_content in properties.items():
            attr_type = prop_content['type']
            attr_schemas_builder = self.builder_provider.get_builder(attr_type)
            attr_schemas[prop_name] = attr_schemas_builder.build_schema(prop_content)
        return attr_schemas

    @staticmethod
    def create_schema_type(attrs):
        """Create schema type from given dictionary of attributes."""
        return type('Object' + str(uuid4()), (NadiaSchema,), attrs)
