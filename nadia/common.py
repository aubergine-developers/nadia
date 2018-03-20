"""Functionalities related to all builders."""
from abc import ABC, abstractmethod


class Builder(ABC):
    """Base class for all field builders.

    :param builder_provider: a provider used for obtaining builders for other OpenAPI types.
    :type bulder_provider: a subclass of :py:class:`nadia.builder_provider.BuilderProvider`
    """
    key = None
    marshmallow_class = None

    def __init__(self, builder_provider):
        self.builder_provider = builder_provider

    @staticmethod
    def translate_args(spec, **kwargs):
        """Translate arguments given in OpenAPI spec to keyword arguments for marshmallow classes.

        :param spec: a dictionary extracted from OpenAPI spec containing definition of some
         object.
        :type spec: dict
        :return: A mapping containing keyword arguments used for constructing marshmallow objects.
        :rtype: dict
        """
        
        return {
            'allow_none': spec.get('nullable', False),
            'required': kwargs.get('required', False)
        }

    @abstractmethod
    def build_schema(self, spec, **kwargs):
        """Build marshmallow schema from definition extracted from OpenAPI specs.

        :param spec: an object definition extracted from OpenAPI specification.
        :return: Schema or a Field constructed from the spec dictionary.
        :rtype: :py:class:`marshmallow.Schema` or :py:class:marshmallow.Field

        .. note:: The return type as well as the nature of the object constructed depends
           on the concrete implementation of Builder. Usually the builder designed for
           handling object types will return Schema object, while builders designed for handling
           other data types will return Field instances.
        """
        pass
