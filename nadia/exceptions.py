"""Common Exceptions."""


class UnknownTypeException(Exception):
    """Exception raised when we encounter unknown datatype in schema.

    Note that circumstances under which this Exception is raised should not
    happen when the schema dict passed was created from valid OpenAPI specification.

    :param typename: name of type that resulted in raising exception.
    :type typename: str
    """
    def __init__(self, typename):
        super(UnknownTypeException, self).__init__(typename)
        self.typename = typename

    def __str__(self):
        return 'Unknown data type: {}'.format(self.typename)
