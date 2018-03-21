"""Test commoon functionallities for field builders."""
import unittest
from ddt import ddt, data
from nadia import primitives


@ddt
class TestPrimitiveBuilder(unittest.TestCase):
    """Test casefor functionallities common to all primitive builder classes."""

    @data(primitives.FloatBuilder,
          primitives.IntegerBuilder,
          primitives.StringBuilder)
    def test_default_args(self, builder):
        """FloatBuilder should set default values as in OpenAPI spec."""
        field = builder.build_schema({})
        self.assertEqual(False, field.allow_none)
        self.assertEqual(False, field.required)
        self.assertIsNone(field.validate)

    @data(primitives.FloatBuilder,
          primitives.IntegerBuilder,
          primitives.StringBuilder)
    def test_nullable(self, builder):
        """Building a Float field should respect nullable settings."""
        for nullable in (True, False):
            field = builder.build_schema({'nullable': nullable})
            self.assertEqual(nullable, field.allow_none)

    @data(primitives.FloatBuilder,
          primitives.IntegerBuilder,
          primitives.StringBuilder)
    def test_required(self, builder):
        """Building a Float field should respect required settings."""
        for required in (True, False):
            field = builder.build_schema({}, required=required)
            self.assertEqual(required, field.required)
