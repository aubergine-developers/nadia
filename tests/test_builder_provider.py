"""Test cases for builder_provider module."""
import unittest
from unittest import mock
from ddt import ddt, data
from nadia.builder_provider import BuilderProvider


@ddt
class TestBuilderProvider(unittest.TestCase):
    """Test case for BuilderProvider."""

    builders_dict = {'type1': mock.Mock(),
                     'type2': mock.Mock()}

    @data('type1', 'type2')
    def test_instantiates_correct_class(self, typename):
        """BuilderProvider should instantiate correct classes."""
        self.builders_dict[typename].reset_mock()
        provider = BuilderProvider(self.builders_dict)

        ret_val = provider.get_builder(typename)
        self.assertEqual(ret_val, self.builders_dict[typename].return_value)
        self.builders_dict[typename].assert_called_once_with(provider)

    def test_instantiates_builders_once(self):
        """BuilderProvider should cache created builder objects."""
        provider = BuilderProvider(self.builders_dict)
        provider.get_builder('type1')
        provider.get_builder('type1')
        self.builders_dict['type1'].assert_called_once_with(provider)
