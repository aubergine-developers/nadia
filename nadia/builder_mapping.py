"""Implementation of class responsible for obtaining schema builders for OpenAPI types."""
import collections
import logging
from nadia.array import ArrayBuilder
from nadia.object import ObjectBuilder
from nadia.primitives import FloatBuilder, IntegerBuilder, StringBuilder


class BuilderMapping(collections.Mapping):
    """Caching mapping of builders."""

    builder_factories = {
        'number': FloatBuilder,
        'integer': IntegerBuilder,
        'string': StringBuilder,
        'object': ObjectBuilder,
        'array': ArrayBuilder}

    def __init__(self, builder_factories=None):
        self._cache = {}
        if builder_factories is not None:
            self.builder_factories = builder_factories

    def __getitem__(self, typename):
        logger = logging.getLogger('nadia.builder_mapping')
        if typename not in self._cache:
            try:
                logger.debug('Constructing builder for type %s.', typename)
                self._cache[typename] = self.builder_factories[typename](self)
            except KeyError:
                logger.error('Unknown type found in specs: %s', typename)
                raise KeyError(f'Unknown type found in specs: {typename}.')
        return self._cache[typename]

    def __iter__(self):
        return iter(self._cache)

    def __len__(self):
        return len(self._cache)