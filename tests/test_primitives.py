"""Test cases for schema generators for primitive types."""
import unittest
from marshmallow import fields
from nadia import primitives


class TestFloatBulder(unittest.TestCase):
    """Test case for FloatBuilder."""

    def test_correct_type(self):
        """Building a Float field return marshmallow.fields.Float."""
        field = primitives.FloatBuilder.build_schema({})
        self.assertEqual(fields.Float, type(field))
