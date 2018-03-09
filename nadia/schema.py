"""Base schema used by Nadia."""
from marshmallow import Schema, validates_schema, ValidationError


class NadiaSchema(Schema):
    """Base marshmallow schema used by Nadia."""

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, _data, original_data):
        """Validator raising ValidationError if extra keys are provided.

        This validator is taken from the the official recipe located at:
        http://marshmallow.readthedocs.io/en/latest/extending.html#validating-original-input-data
        """
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)
