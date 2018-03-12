"""Implementation of schema builder for object type."""
from uuid import uuid4
from marshmallow import fields
from nadia.schema import NadiaSchema
from nadia.common import Builder


class ObjectBuilder(Builder):
    """Schema builder for object datatype."""

    def build_schema(self, spec):
        """Build Schema from a definition of OpenAPI object.

        :param spec: a mapping containing object definition extracted from OpenAPI spec.
        :type spec: dict
        :return: Schema constructed from `spec`.
        :rtype: :py:class:`marshmalow.Schema`
        """
        attrs = self.construct_attributes_schemas(spec['properties'])
        obj_schema = self.create_schema_type(attrs)
        return fields.Nested(obj_schema, **self.translate_args(spec))

    def construct_attributes_schemas(self, properties):
        """Construct Schemas corresponding to object properties.

        This method is used to construct attributes of the object schema being constructed.

        :param properties: a dictionary of properties extracted from OpenAPI object's definition.
        :type properties: dict
        :return: a mapping property-name -> Schema or Field.
        :rtype: dict
        """
        attr_schemas = {}
        for prop_name, prop_content in properties.items():
            attr_type = prop_content['type']
            attr_schemas_builder = self.builder_provider.get_builder(attr_type)
            attr_schemas[prop_name] = attr_schemas_builder.build_schema(prop_content)
        return attr_schemas

    @staticmethod
    def create_schema_type(attrs):
        """Create schema type from given dictionary of attributes.

        :param attrs: mapping of attributes of the newly created Python type.
        :type attrs: dict
        :return: newly created type with randomly choosen name and single base class -
         :py:class:`nadia.NadiaSchema`.
        :rtype: type
        """
        return type('Object' + str(uuid4()), (NadiaSchema,), attrs)
