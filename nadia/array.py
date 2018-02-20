"""Implementation of validation builder for array type."""
from marshmallow import fields
from nadia.common import Builder


class ArrayBuilder(Builder):
    """Schema builder for array datatype."""

    def build_schema(self, spec_dict):
        """Build Marshmallow schema for array datatype."""
        field_args = self.translate_args
        item_body = spec_dict['items']
        item_builder = self.builder_provider.get_builder(item_body['type'])
        return fields.List(item_builder.build_schema(item_body), **self.translate_args(spec_dict))
