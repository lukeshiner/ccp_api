"""Base class for Cloud Commerce Pro API endpoints."""

import zeep

from .credentials import Credentials
from .exceptions import ResponseError


class Endpoint(zeep.client.Client):
    """Wrapper for Cloud Commerce Pro API endpoints."""

    LIVE_BASE_DOMAIN = "wcfccpservicesbase.cloudcommercepro.com"
    SANDBOX_BASE_DOMAIN = "wcfccpservicesbase.cloudcommercepro.com"

    def __init__(self):
        """Set up the endpoint."""
        self.login = Credentials()
        super().__init__(wsdl=self.wsdl_url())

    def wsdl_url(self):
        """Return the URL of the endpoiint wsdl file."""
        return "http://{}/{}.svc?wsdl".format(self.SANDBOX_BASE_DOMAIN, self.ENDPOINT)

    def credentials(self):
        """Return API credentials formatted for use in requests."""
        if self.login.brand_id is None or self.login.security_hash is None:
            raise ValueError("No login credentials set")
        return {
            "BrandID": self.login.brand_id,
            "SecurityHash": self.login.security_hash,
        }

    def call_method(self, method_name, content):
        """Make a request to one of the endpoint's methods."""
        request_content = self.credentials()
        request_content["Content"] = content
        with self.settings(raw_response=self.login.raw_response):
            response = getattr(self.service, method_name)(request_content)
        return response


class _Method:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def call(self, *args, **kwargs):
        content = self.process_content(*args, **kwargs)
        try:
            response = self.endpoint.call_method(self.method_name, content)
        except Exception as e:
            self.handle_request_exception(e)
        if self.endpoint.login.raw_response is True:
            return response
        else:
            self.check_response(response)
            return self.process_response(response)

    def check_response(self, response):
        if not response.Success:
            raise ResponseError(response.ErrorMessage)

    def process_content(self, *args, **kwargs):
        if args:
            return args[0]
        else:
            return None

    def process_response(self, response):
        return response.Content

    def handle_request_exception(self, e):
        raise e
