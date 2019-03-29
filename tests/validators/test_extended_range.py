"""Test cases for nadia.validators.extended_range"""
from marshmallow.validate import ValidationError
import pytest
from nadia.validators import extended_range

@pytest.mark.parametrize(
    'value,min_value,exclusive',
    [[5.0, 5.0, False],
     [3.7, 2.1, True],
     [3.7, 2.1, False],
     [4, 3, True],
     [-2, -2, False]])
def test_accepts_minimum(value, min_value, exclusive):
    """The extended_range should accept correct values in minimum-only setup."""
    validate = extended_range(min_value=min_value, exclusive_min=exclusive)
    assert validate(value) == value

@pytest.mark.parametrize(
    'value,max_value,exclusive',
    [[3, 5, False],
     [3, 4, True],
     [5, 5, False],
     [-3.0, 1.5, False],
     [2.0, 2.0, False]])
def test_accepts_maximum(value, max_value, exclusive):
    """The extended_range should accept correct values in maximum-only setup."""
    validate = extended_range(max_value=max_value, exclusive_min=exclusive)
    assert validate(value) == value

@pytest.mark.parametrize(
    'value,min_value,max_value,exclusive_min,exclusive_max',
    [[3, -2, 4, False, False],
     [-2.1, -2.1, 1.0, False, True],
     [-2.1, -2.1, 2.0, False, True],
     [105, 100, 105, True, False],
     [105, 100, 105, False, False]])
def test_accepts_range(value, min_value, max_value, exclusive_min, exclusive_max):
    """The extended_range should accept correct values in minimum + maximum setup."""
    validate = extended_range(
        min_value=min_value,
        max_value=max_value,
        exclusive_min=exclusive_min,
        exclusive_max=exclusive_max)
    assert validate(value) == value

def test_rejects_lesser_inclusive():
    """The extended_range should reject values lesser than min when min is inclusive."""
    validate = extended_range(min_value=11.0)
    with pytest.raises(ValidationError) as exc_info:
        validate(9.0)
    assert 'Value must be >= 11.0' in str(exc_info.value)

def test_rejects_below_range_inclusive():
    """The extended_range should reject values below given range when min is inclusive."""
    validate = extended_range(min_value=13, max_value=200, exclusive_max=True)
    with pytest.raises(ValidationError) as exc_info:
        validate(12)
    assert 'Value must be in the interval [13, 200)' in str(exc_info.value)

def test_rejects_lesser_exclusive():
    """The extended_range should reject values lesser or equal to min when min is exclusive."""
    validate = extended_range(min_value=-3.5, exclusive_min=True)
    with pytest.raises(ValidationError) as exc_info:
        validate(-3.5)
    assert 'Value must be > -3.5' in str(exc_info.value)

def test_rejects_below_range_exclusive():
    """The extended_range should reject values below given range when min is exclusive."""
    validate = extended_range(min_value=420, max_value=500, exclusive_min=True)
    with pytest.raises(ValidationError) as exc_info:
        validate(300)
    assert 'Value must be in the interval (420, 500]' in str(exc_info.value)

def test_rejects_greater_inclusive():
    """The extended_range should reject values greater than max when max is inclusive."""
    validate = extended_range(max_value=1023)
    with pytest.raises(ValidationError) as exc_info:
        validate(2048)
    assert 'Value must be <= 1023' in str(exc_info.value)

def test_rejects_above_range_inclusive():
    """The extended_range should reject values above given range when min is inclusive."""
    validate = extended_range(min_value=-69, max_value=0, exclusive_min=True)
    with pytest.raises(ValidationError) as exc_info:
        validate(1)
    assert 'Value must be in the interval (-69, 0]' in str(exc_info.value)

def test_rejects_greater_exclusive():
    """The extended_range should reject values greater or equal to max, when max is exclusive."""
    validate = extended_range(max_value=600, exclusive_max=True)
    with pytest.raises(ValidationError) as exc_info:
        validate(600)
    assert 'Value must be < 600' in str(exc_info.value)

def test_rejects_above_range_exclusive():
    """The extended_range should reject values above given range when min is inclusive."""
    validate = extended_range(min_value=500, max_value=600, exclusive_max=True)
    with pytest.raises(ValidationError) as exc_info:
        validate(700)
    assert 'Value must be in the interval [500, 600)' in str(exc_info.value)
