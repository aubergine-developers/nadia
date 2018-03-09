"""Implementation of class responsible for obtaining schema builders for OpenAPI types."""
import logging
from functools import lru_cache
from nadia.array import ArrayBuilder
from nadia.object import ObjectBuilder
from nadia.primitives import FloatBuilder, IntegerBuilder, StringBuilder
from nadia.exceptions import UnknownTypeException


class BuilderProvider(object):
    """Class for providing builders for various data types.

    :param builders: mapping between OpenAPI types and classes implementing builder
     interface for them.
    :type builders: dict

    .. note:: The purpose of this class is to act as a mapping between types and
       corresponding builders, while elegantly handling unknown types and lazy creation
       of the builders. It is injected as a dependency in :py:class:`nadia.api.SchemaBuilder`.
    """
    def __init__(self, builders):
        self.builders = builders

    @lru_cache(maxsize=None)
    def get_builder(self, typename):
        """Get builder instance for given OpenAPI type.

        :param typename: OpenAPI type for which to get a builder.
        :type typename: str
        :return: a builder corresponding to given type.
        :rtype: a subclass of :py:class:`nadia.common.Builder`
        :raises: :py:exc:`nadia.exceptions.UnknownTypeException` if typename does not
         correspond to known OpenAPI type.
        """
        if typename not in self.builders:
            raise UnknownTypeException(typename)
        self.logger.info('Constructing builder for type: %s.', typename)
        return self.builders[typename](self)

    @property
    def logger(self):
        """Logger used by this BuilderProvider."""
        return logging.getLogger('BuilderProvider')

    @staticmethod
    def get_default():
        """Construct BuilderProvider with default builders.

        :rtype: :py:class:`nadia.builder_provider.BuilderProvider`
        """
        return BuilderProvider({
            'number': FloatBuilder,
            'integer': IntegerBuilder,
            'string': StringBuilder,
            'object': ObjectBuilder,
            'array': ArrayBuilder})
