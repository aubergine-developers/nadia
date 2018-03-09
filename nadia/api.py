"""The nadia public api."""
from uuid import uuid4
from nadia.builder_provider import BuilderProvider
from nadia.schema import NadiaSchema


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
