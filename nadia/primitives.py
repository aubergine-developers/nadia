"""Schema generators for primitive types."""
from marshmallow import fields
from nadia.common import Builder


class PrimitiveBuilder(Builder):
    """Base class for primitive fields builder."""
    key = None
    marshmallow_class = None

    @classmethod
    def build_schema(cls, spec, **kwargs):
        """Build a Field for a primitive object.

        .. seealso: :py:meth:`nadia.common.Builder.build_schema`

        .. note :: Conforming to the base class documentation, this method returns
           instances of :py:class:`marshmallow.Field`.
        """
        return cls.marshmallow_class(**cls.translate_args(spec, **kwargs))

class FloatBuilder(PrimitiveBuilder):
    """Float schema builder.

    This builder is designed for constructing schemas for OpenAPI `number` type.
    """
    key = 'number'
    marshmallow_class = fields.Float


class IntegerBuilder(PrimitiveBuilder):
    """Integer schema builder.

    This builder is designed for constructing schemas for OpenAPI 'integer' type.
    """
    key = 'integer'
    marshmallow_class = fields.Integer


class StringBuilder(PrimitiveBuilder):
    """Str schema builder.

    This builder is designed for constructing schemas for OpenAPI 'string' type.
    """
    key = 'string'
    marshmallow_class = fields.String
