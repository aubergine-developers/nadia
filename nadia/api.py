"""The nadia public api."""
from uuid import uuid4
from nadia.builder_provider import BuilderProvider
from nadia.schema import NadiaSchema, NadiaCombinedSchema


class SchemaBuilder(object):
    """Class used for building schemas from given specification dict.

    :param builder_provider: an object providing builders via get_builder method.
     Typically an instance of :py:class:`nadia.builder_provider.BuilderProvider`.
    """

    def __init__(self, builder_provider):
        self.builder_provider = builder_provider

    def build(self, spec):
        """Build schema from given specification dict.

        :param spec: a dictionary containing specification of the object for which
         Schema should be build.
        :type spec: dict
        :return: Schema corresponding to the object defined by spec
        :rtype: :py:class:`marshmallow.Schema`
        """

        if self.is_combined_schema(spec):
            combination = list(spec.keys())[0]
            specs = spec[combination]
            schemas = {schema[0]: self.build(schema[1]) for schema in specs.items()}
            attrs = {'content': schemas, 'combination': combination}
            return type('Object' + str(uuid4()), (NadiaCombinedSchema, ), attrs)

        else:
            content_builder = self.builder_provider.get_builder(spec.get('type', 'object'))
            attrs = {'content':  content_builder.build_schema(spec)}
            return type('Object' + str(uuid4()), (NadiaSchema, ), attrs)()

    @staticmethod
    def create():
        """Create SchemaBuilder.

        :rtype: :py:class:`nadia.api.SchemaBuilder`

        .. note:: This method is designed to be further extended as a factory method.
           Later it should be able to accept some parameters governing creation of the
           SchemaBuilder. Currently it creates :py:class:`nadia.api.SchemaBuilder`
           by passing default instance of :py:class:`nadia.builder_provider.BulderProvider`
           to initializer.
        """
        provider = BuilderProvider.get_default()
        return SchemaBuilder(provider)

    @staticmethod
    def is_combined_schema(spec):
        """Check if provided schema specification is a combination of schemas."""
        combined_schemas = ["oneOf", "anyOf", "allOf"]
        spec_keys = spec.keys()

        return len(spec_keys) == 1 and not spec_keys.isdisjoint(combined_schemas)
