"""Custom validators for use with nadia."""
from marshmallow.validate import ValidationError
from operator import gt, lt, ge, le

def extended_range(min_value=None, max_value=None, exclusive_min=False, exclusive_max=False):
    """Create validator checking if number lies in the given interval.

    :param min_value: lower end of the interval. If `None` given, lower end will not be checked on
     validation. This would result in the target interval being (-inf, max) or (-inf, max].
    :type min_value: number
    :param max_value: upper end of the interval. If `None` given, upper end will not be checked on
     validation.
    :type min_value: number
    :param exclusive_min: if the lower end of the interval should be exclusive. If yes,
     < comparison will be used, otherwise the comparison operator is <=.
    :type exclusive_min: bool
    :param exclusive_max: analogous to `exclusive_min` but for upper end.
    :type exclusive_max: bool
    :raises ValueError: if both `min` and `max` are `None`
    """
    if min_value is None and max_value is None:
        raise ValueError('You need to provide min or max to construct ExtendedRange.')

    lesser_op = le if exclusive_min else lt
    greater_op = ge if exclusive_max else gt

    if min_value is not None and max_value is None:
        relation_str = f'> {min_value}' if exclusive_min else f'>= {min_value}'
    elif min_value is None:
        relation_str = f'< {max_value}' if exclusive_max else f'<= {max_value}'
    else:
        left = '(' if exclusive_min else '['
        right = ')' if exclusive_max else ']'
        relation_str = f'in the interval {left}{min_value}, {max_value}{right}'

    error_message = f'Value must be {relation_str}.'

    def _validate(value):
        if min_value is not None and lesser_op(value, min_value):
            raise ValidationError(error_message)

        if max_value is not None and greater_op(value, max_value):
            raise ValidationError(error_message)

        return value

    return _validate

def collection_size_range(min_size=None, max_size=None):
    """Create validator checking if number of items in the collection lies in the given range.

    :param min: minimum number of items. If `None` given, number of items is not bounded
     from below.
    :type min: int
    :param max: maximum number of items. If `None` given, number of items is not bounded
     from above.
    :type max: int
    :raises ValueError: if both `min` and `max` are `None`
    """
    if min_size is None and max_size is None:
        raise ValueError('You need to provide min or max to construct ExtendedRange.')

    if min_size is not None and max_size is None:
        relation_str = f'>= {min_size}'
    elif min_size is None:
        relation_str = f'<= {max_size}'
    else:
        relation_str = f'between {min_size} and {max_size}'

    error_message = f'Number of items must be {relation_str}.'

    def _validate(collection):
        if min_size is not None and len(collection) < min_size:
            raise ValidationError(error_message)

        if max_size is not None and len(collection) > max_size:
            raise ValidationError(error_message)

        return collection

    return _validate

def unique_items(sequence):
    """Validator returning boolean value indicating if sequence contains unique elements.

    :param sequence: sequence of elements to validate.
    :type sequence: sequence of arbitrary objects.
    :returns: sequence
    :raises ValidationError: if elements in the sequence are not unique.

    .. note::
       This validators works efficiently only in case sequence contains hashable elements.
       If this is not the case, it resorts to pairwise comparisons, which is O(len(sequence)**2).
    """
    try:
        if len(sequence) != len(set(sequence)):
            raise ValidationError('Elements are not unique.')
    # If it turns out sequence contains nonhashable objects, we need to resort to
    # naive pairwise comparison.
    except TypeError:
        for i in range(len(sequence)): # pylint: disable=consider-using-enumerate
            for j in range(i+1, len(sequence)):
                if sequence[i] == sequence[j]:
                    raise ValidationError('Elements are not unique.')
    return sequence
