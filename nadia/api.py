"""The nadia public api."""
from uuid import uuid4
from nadia.builder_mapping import BuilderMapping
from nadia.schema import NadiaSchema, NadiaCombinedSchema


def build_schema(spec, builder_mapping=BuilderMapping()):
    """Build schema from given OpenAPI specification.

    :param spec: mapping with OpenAPI specification
    :type spec: Mapping[string, Any]
    :param builder_mapping: a mapping typename -> factory, used to create builders
     for specific types. Every value (factory) should be a callable accepting
     builder_mapping as an argument and producing builder object.
    :type builder_mapping: Mapping[string, Callable]
    :returns: marshmallow schema constructed for given specification.
    :rtype: :py:class:`marshmallow.Schema`
    """

    combined_schemas = ("oneOf", "anyOf", "allOf")

    if is_combined_schema(spec):
        combination = list(spec.keys())[0]
        specs = spec[combination]
        schemas = {schema[0]: self.build(schema[1]) for schema in specs.items()}
        attrs = {'content': schemas, 'combination': combination}
        return type('Object' + str(uuid4()), (NadiaCombinedSchema, ), attrs)

    else:
        content_builder = builder_mapping[spec.get('type', 'object')]
        attrs = {'content':  content_builder.build_schema(spec)}
        return type('Object' + str(uuid4()), (NadiaSchema, ), attrs)()   
  

def is_combined_schema(spec):
    """Check if provided schema specification is a combination of schemas."""
    spec_keys = spec.keys()

    return len(spec_keys) == 1 and not spec_keys.isdisjoint(SchemaBuilder.combined_schemas)
