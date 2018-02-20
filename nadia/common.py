"""Common functionallities related to all builders."""
from abc import ABC, abstractmethod


class Builder(ABC):
    """Base class for all field builders."""

    key = None
    marshmallow_class = None

    def __init__(self, builder_provider):
        self.builder_provider = builder_provider

    @classmethod
    def translate_args(cls, spec_dict):
        """Translate."""
        return {
            'allow_none': spec_dict.get('nullable', False),
            'required': spec_dict.get('required', False)
        }

    @abstractmethod
    def build_schema(self, spec_dict):
        """Build marshmallow schema fromschema dictionary extracted from OpenAPI specs."""
        pass
