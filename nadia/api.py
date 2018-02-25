"""Main builder class."""
from uuid import uuid4
from marshmallow import Schema
from nadia.builder_provider import BuilderProvider
from nadia.schema import NadiaSchema


class SchemaBuilder(object):
    """Class used for building schemas for given specification dict."""


    def __init__(self, builder_provider):
        self.builder_provider = builder_provider

    def build(self, spec_dict):
        """Build schema for given specification dict."""
        content_builder = self.builder_provider.get_builder(spec_dict.get('type', 'object'))
        attrs = {'content':  content_builder.build_schema(spec_dict)}
        return type('Object' + str(uuid4()), (NadiaSchema, ), attrs)()

    @staticmethod
    def create():
        """Create SchemaBuilder.

        Note: this method is designed to be further extended as a factory method.
        Later it should be able to accept some parameters ogerning creation of the
        SchemaBuilder.
        """
        provider = BuilderProvider.get_default()
        return SchemaBuilder(provider)
