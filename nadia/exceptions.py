"""Module with common Exceptions."""


class UnknownTypeException(Exception):
    """Exception raised when we encounter unknown datatype in schema.

    Note that circumstances under which this Exception is raised should not
    happend when the schema dict passed was created from valid OpenAPI specification.
    """

    def __init__(self, typename):
        super(UnknownTypeException, self).__init__(typename)
        self.typename = typename

    def __str__(self):
        return 'Unknown data type: {}'.format(typename)
