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
