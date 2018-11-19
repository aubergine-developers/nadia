"""Test cases for builder_mapping module."""
import unittest
from unittest import mock
from ddt import ddt, data
from nadia.builder_mapping import BuilderMapping


@ddt
class TestBuilderMapping(unittest.TestCase):
    """Test case for BuilderMapping."""

    builders_dict = {'type1': mock.Mock(),
                     'type2': mock.Mock()}

    @data('type1', 'type2')
    def test_instantiates_correct_class(self, typename):
        """BuilderMapping should instantiate correct classes."""
        self.builders_dict[typename].reset_mock()
        mapping = BuilderMapping(self.builders_dict)

        ret_val = mapping[typename]
        self.assertEqual(ret_val, self.builders_dict[typename].return_value)
        self.builders_dict[typename].assert_called_once_with(mapping)

    def test_instantiates_builders_once(self):
        """BuilderMapping should cache created builder objects."""
        mapping = BuilderMapping(self.builders_dict)
        mapping.get('type1')
        mapping.get('type1')
        self.builders_dict['type1'].assert_called_once_with(mapping)
