"""Test cases for nadia.validators.CollectionSizeRange"""
from marshmallow.validate import ValidationError
import pytest
from nadia.validators import CollectionSizeRange


@pytest.mark.parametrize(
    'collection,min_size',
    [[(1, 2, 3), 2],
     [[2, 3, 4, 5], 4],
     [{2, 1, 3, 7}, 0],
     [{0: 3, 1: 'test'}, 1]])
def test_accepts_minimum_size(collection, min_size):
    """CollectionSizeRange should accept collections of correct size in min-size-only setup."""
    validate = CollectionSizeRange(min_size=min_size)
    assert validate(collection) == collection

@pytest.mark.parametrize(
    'collection,max_size',
    [[(4, 2, 0), 10],
     [[5, -3, 0, 2], 4],
     [{-2.5, 3.4, 2.1}, 5]])
def test_accepts_maximum_size(collection, max_size):
    """CollectionSizeRange should accept collections of correct size in max-size-only setup."""
    validate = CollectionSizeRange(max_size=max_size)
    assert validate(collection) == collection

@pytest.mark.parametrize(
    'collection,min_size',
    [[(4, 2, 0), 4],
     [[5, -3, 0, 2], 5],
     [{-2.5, 3.4, 2.1}, 5]])
def test_rejects_too_small(collection, min_size):
    """CollectionSizeRange should reject too large collections in max-size-only setup."""
    validate = CollectionSizeRange(min_size=min_size)
    with pytest.raises(ValidationError) as exc_info:
        validate(collection)

    assert f'Number of items must be >= {min_size}' in str(exc_info.value)

@pytest.mark.parametrize(
    'collection,max_size',
    [[(1, 2, 3), 2],
     [[2, 3, 4, 5], 3],
     [{2, 1, 3, 7}, 2],
     [{0: 3, 1: 'test'}, 1]])
def test_rejects_too_large(collection, max_size):
    """CollectionSizeRange should reject too large collections in max-size-only setup."""
    validate = CollectionSizeRange(max_size=max_size)

    with pytest.raises(ValidationError) as exc_info:
        validate(collection)

    assert f'Number of items must be <= {max_size}' in str(exc_info.value)

@pytest.mark.parametrize(
    'collection,min_size,max_size',
    [[(-3, 2, 4, 0, 5), 3, 7],
     [[2, 3], 1, 4],
     [{}, 0, 10]])
def test_accepts_in_range(collection, min_size, max_size):
    """CollectionSizeRange should accept collections with number of items in specified range."""
    validate = CollectionSizeRange(min_size=min_size, max_size=max_size)
    assert validate(collection) == collection

@pytest.mark.parametrize(
    'collection,min_size,max_size',
    [[(-3, 2, 4, 0, 5), 1, 4],
     [[2, 3], 3, 4],
     [{}, 2, 10]])
def test_rejects_out_of_range(collection, min_size, max_size):
    """CollectionSizeRange should reject collections with number of items outside specified range."""
    validate = CollectionSizeRange(min_size=min_size, max_size=max_size)

    with pytest.raises(ValidationError) as exc_info:
        validate(collection)

    assert f'Number of items must be between {min_size} and {max_size}' in str(exc_info.value)
