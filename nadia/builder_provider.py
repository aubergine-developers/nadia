"""Builder provider that should be injected to builder classes."""
import logging
from functools import lru_cache
from nadia.array import ArrayBuilder
from nadia.object import ObjectBuilder
from nadia.primitives import FloatBuilder, IntegerBuilder, StringBuilder
from nadia.exceptions import UnknownTypeException


class BuilderProvider(object):
    """Class for providing builders for given data type."""

    def __init__(self, builders_dict):
        self.builders_dict = builders_dict

    @lru_cache(maxsize=None)
    def get_builder(self, typename):
        """Get builder for given type name."""
        if typename not in self.builders_dict:
            raise UnknownTypeException(typename)
        self.logger.info('Constructing builder for type: %s.', typename)
        return self.builders_dict[typename](self)

    @property
    def logger(self):
        """Logger used by this BuilderProvider."""
        return logging.getLogger('BuilderProvider')

    @staticmethod
    def get_default():
        return BuilderProvider({
            'number': FloatBuilder,
            'integer': IntegerBuilder,
            'string': StringBuilder,
            'object': ObjectBuilder,
            'array': ArrayBuilder})
