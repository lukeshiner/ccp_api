"""Exceptions for ccp_api."""


class ResponseError(Exception):
    """Raised when an API method returns an error message."""

    def __init__(self, message):
        """Raise exception with the error message returned from the API call."""
        super().__init__("Request returned error: {}".format(message))
