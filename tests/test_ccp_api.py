"""Tests for ccp_api."""

import ccp_api
import pytest

from .base_tests import Base_ccp_api_Test


class TestCCPAPI(Base_ccp_api_Test):
    @pytest.fixture
    def error_response(self, file_fixture):
        return file_fixture("error_response.xml")

    def test_login(self):
        ccp_api.login.set(
            brand_id=self.TEST_BRAND_ID, security_hash=self.TEST_SECURITY_HASH
        )
        assert ccp_api.login.brand_id == self.TEST_BRAND_ID
        assert ccp_api.login.security_hash == self.TEST_SECURITY_HASH

    def test_error_response_raises_ResponseError(
        self, requests_mock, file_fixture, error_response
    ):
        requests_mock.post(
            ccp_api.products.wsdl_url(), text=file_fixture("products", "wsdl.xml")
        )
        requests_mock.post(
            "http://wcfccpservicesbase.cloudcommercepro.com/CCPApiProductsService.svc",
            text=error_response,
        )
        with pytest.raises(ccp_api.exceptions.ResponseError):
            ccp_api.products.get_product_by_ID("1234864")
