class ClientException(Exception):
    """The base exception for everything to do with clients."""
    message = None

    def __init__(self, status_code=None, message=None, errors=None):
        self.status_code = status_code
        self.errors = errors
        if not message:
            if self.message:
                message = self.message
            else:
                message = self.__class__.__name__
        super(Exception, self).__init__(message)
