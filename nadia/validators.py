"""Custom validators for use with nadia."""
from marshmallow.validate import ValidationError
from operator import gt, lt, ge, le

class ExtendedRange:
    """Validator checking if number lies in the given interval, possibly with exclusive endpoints.

    :param min: lower end of the interval. If `None` given, lower end will not be checked on
     validation. This would result in the target interval being (-inf, max) or (-inf, max].
    :type min: number
    :param max: upper end of the interval. If `None` given, upper end will not be checked on
     validation.
    :param exclusive_min: if the lower end of the interval should be exclusive. If yes,
     < comparison will be used, otherwise the comparison operator is <=.
    :type exclusive_min: bool
    :param exclusive_max: analogous to `exclusive_min` but for upper end.
    :type exclusive_max: bool
    :raises ValueError: if both `min` and `max` are `None`
    """
    def __init__(self, min=None, max=None, exclusive_min=False, exclusive_max=False):
        if min is None and max is None:
            raise ValueError('You need to provide min or max to construct ExtendedRange.')

        self.lesser_op = le if exclusive_min else lt
        self.greater_op = ge if exclusive_max else gt
        self.min = min
        self.max = max

        if self.min is not None and self.max is None:
            relation_str = f'> {min}' if exclusive_min else f'>= {min}'
        elif self.min is None:
            relation_str = f'< {max}' if exclusive_max else f'<= {max}'
        else:
            left = '(' if exclusive_min else '['
            right = ')' if exclusive_max else ']'
            relation_str = f'in the interval {left}{min}, {max}{right}'

        self.error_message = f'Value must be {relation_str}.'

    def __call__(self, value):
        if self.min is not None and self.lesser_op(value, self.min):
            raise ValidationError(self.error_message)

        if self.max is not None and self.greater_op(value, self.max):
            raise ValidationError(self.error_message)

        return value

class CollectionSizeRange:
    """Validator checking if number of items in the collection lies in the given range.

    :param min: minimum number of items. If `None` given, number of items is not bounded
     from below.
    :type min: int
    :param max: maximum number of items. If `None` given, number of items is not bounded
     from above.
    :type max: int
    :raises ValueError: if both `min` and `max` are `None`
    """
    def __init__(self, min_size=None, max_size=None):
        if min is None and max is None:
            raise ValueError('You need to provide min or max to construct ExtendedRange.')

        self.min_size = min_size
        self.max_size = max_size

        if self.min_size is not None and self.max_size is None:
            relation_str = f'>= {min_size}'
        elif self.min_size is None:
            relation_str = f'<= {max_size}'
        else:
            relation_str = f'between {min_size} and {max_size}'

        self.error_message = f'Number of items must be {relation_str}.'

    def __call__(self, collection):
        if self.min_size is not None and len(collection) < self.min_size:
            raise ValidationError(self.error_message)

        if self.max_size is not None and len(collection) > self.max_size:
            raise ValidationError(self.error_message)

        return collection
