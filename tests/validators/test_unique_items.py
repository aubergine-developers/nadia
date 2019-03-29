"""Test cases for nadia.validators.unique_items."""
from marshmallow.validate import ValidationError
import pytest
from nadia.validators import unique_items


def test_accepts_unique_hashable():
    """The unique_items should accept sequences with unique hashable items."""
    sequence = [1, 2, 3, (1, 0), -2.5, "test"]
    assert sequence == unique_items(sequence)

def test_accepts_unique_nonhashable():
    """The unique_items should accept sequences with unique items even if they are not hashable."""
    sequence = [0, 1, {0: 'foo', 1: 'bar'}, {2: 'baz'}, {0: 'x', 1: 'y'}]
    assert sequence == unique_items(sequence)

def test_rejects_nonunique_hashable():
    """The unique_items should reject sequences with nonunique hashable items."""
    sequence = [0, 2.0, 0, -1.5]

    with pytest.raises(ValidationError) as exc_info:
        unique_items(sequence)

    assert 'Elements are not unique.' == str(exc_info.value)

def test_rejects_nonunique_nonhashable():
    """The unique_items should reject sequences with nonunique nonhashable items."""
    sequence = [1.0, 2, {'foo': 2, 'bar': 3}, {'foo': 2, 'bar': 3}]

    with pytest.raises(ValidationError) as exc_info:
        unique_items(sequence)

    assert 'Elements are not unique.' == str(exc_info.value)
