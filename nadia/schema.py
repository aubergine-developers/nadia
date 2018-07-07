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


class NadiaCombinedSchema(object):
    """Class used to process combined schemas, using anyOf, allOf and oneOf."""

    @classmethod
    def validate(cls, data):
        """Validate a combination of schemas."""
        validation_results = {}
        for name, schema in cls.content.items():
            validation_results[name] = schema.validate(data)

        valid_count = cls.get_valid_count(validation_results)

        if cls.combination == "anyOf" and valid_count > 0:
            return {}
        elif cls.combination == "oneOf" and valid_count == 1:
            return {}
        elif cls.combination == "allOf" and valid_count == len(cls.content):
            return {}
        else:
            return {'content': validation_results}

    @staticmethod
    def get_valid_count(val_results):
        """Check how many validated schemas are valid."""
        results = [result == {} for result in val_results.values()]
        return sum(results)

