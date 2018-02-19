"""Schema generators for primitive types."""
from abc import ABC, abstractmethod
from marshmallow import fields
from nadia.common import Builder


class PrimitiveBuilder(Builder):
    """Base class for primitive fields builder."""
    key = None
    marshmallow_class = None

    @classmethod
    def build(cls, spec_dict):
        """Build a field using given dict read from OpenAPI specification."""
        return cls.marshmallow_class(**cls.translate_args(spec_dict))

    @classmethod
    def build_array(cls, spec_dict, _builder_factory):
        return fields.List(cls.marshmallow_class, **cls.translate_args(spec_dict))


class FloatBuilder(PrimitiveBuilder):
    """Float field builder."""
    key = 'number'
    marshmallow_class = fields.Float


class IntegerBuilder(PrimitiveBuilder):
    """Integer field builder."""
    key = 'integer'
    marshmallow_class = fields.Integer


class StringBuilder(PrimitiveBuilder):
    """Str field builder."""
    key = 'string'
    marshmallow_class = fields.String
