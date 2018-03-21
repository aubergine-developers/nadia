"""Functionalities related to building schemas for array type."""
from marshmallow import fields
from nadia.common import Builder


class ArrayBuilder(Builder):
    """Schema builder for array datatype."""

    def build_schema(self, spec, **kwargs):
        """Build Marshmallow schema for array datatype.

        :param spec: specification of array for which Schema should be build.
        :type spec: dict
        :returns: a List field constructed such that its properties correspond to the ones
         defined in `spec`.
        :rtype: :py:class:`marshmallow.fields.List`
        """
        item_body = spec['items']
        item_builder = self.builder_provider.get_builder(item_body['type'])
        return fields.List(item_builder.build_schema(item_body), **self.translate_args(spec, **kwargs))
