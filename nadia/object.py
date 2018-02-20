"""Implementation of validation builder for object type."""
from uuid import uuid4
import marshmallow
from marshmallow import fields
from nadia.common import Builder


class ObjectBuilder(Builder):
    """Validator builder for array datatype."""

    def build_schema(self, spec_dict):
        """Build validator for custom object datatype."""
        obj_schema = type(
            name='Object' + uuid4(),
            basis=[marshmallow.Schema],
            dict=self.construct_attributes_validators(spec_dict['properties']))
        return fields.Nested(obj_schema, **self.translate_args(spec_dict))

    def construct_attributes_validators(self, properties):
        """Construct dictionary of validators corresponding to object properties dict."""
        attr_validators = {}
        for prop_name, prop_content in properties.items():
            attr_type = prop_content['type']
            attr_validator_builder = self.builder_provider.get_builder(attr_type)
            attr_validators[prop_name] = attr_validator_builder.build_validator(prop_content)
        return attr_validators
