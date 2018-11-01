"""Tests for ccp_api."""

import ccp_api
import pytest
import requests

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
            ccp_api.products.get_product_images("1234864")

    def test_raw_response(self, requests_mock, file_fixture):
        ccp_api.login.raw_response = True
        response_text = file_fixture("products", "get_product_images_response.xml")
        requests_mock.post(
            ccp_api.products.wsdl_url(), text=file_fixture("products", "wsdl.xml")
        )
        requests_mock.post(
            "http://wcfccpservicesbase.cloudcommercepro.com/CCPApiProductsService.svc",
            text=response_text,
        )
        returned_value = ccp_api.products.get_product_images("1234864")
        assert isinstance(returned_value, requests.models.Response)
        assert returned_value.text == response_text
