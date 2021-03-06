"""Base test classes."""

import os
import tempfile
from pathlib import Path

import ccp_api
import pytest
import yaml


class Base_ccp_api_Test:
    """The base test class for ccp_api tests."""

    FIXTURES_DIR = Path(__file__).parent / "fixtures"

    TEST_BRAND_ID = 983
    TEST_SECURITY_HASH = (
        "7,74,108,81,194,157,168,218,184,202,224,10,95,184,85,16,28,209,114,254,32,202,"
        "85,152,20,99,232,90,194,5,106,69,104,244,93,107,237,16,42,78,3,130,140,24,18,"
        "115,67,25,232,205,99,191,67,48,60,201,105,18,25,222,81,24,243,163,94,246,246,"
        "108,132,18,63,151,253,255,130,46,211,207,51,118,81,235,26,77,214,87,167,149,"
        "155,97,100,73,228,227,194,75,5,234,10,77,113,154,244,72,102,188,73,181,20,216,"
        "188,219,254,116,86,48,107,247,77,98,51,88,173,129,217,198,75,247"
    )

    @classmethod
    def setup_method(cls):
        ccp_api.login.set(
            brand_id=cls.TEST_BRAND_ID, security_hash=cls.TEST_SECURITY_HASH
        )

    @classmethod
    def teardown_method(cls):
        ccp_api.login.reset()

    @pytest.fixture
    def tmp_cwd(self):
        os.chdir(tempfile.mkdtemp())

    @pytest.fixture
    def config_file(self, tmp_cwd):
        config = {
            "brand_id": self.TEST_BRAND_ID,
            "security_hash": self.TEST_SECURITY_HASH,
        }
        with open(ccp_api.credentials.CredentialsFile.CREDENTIALS_FILE_NAME, "w") as f:
            yaml.dump(config, f, default_flow_style=False)

    @pytest.fixture
    def mock_product_method(self, requests_mock, products_wsdl):
        def _mock_product_method(**kwargs):
            method_url = (
                "http://wcfccpservicesbase.cloudcommercepro.com/"
                "CCPApiProductsService.svc"
            )
            requests_mock.post(ccp_api.products.wsdl_url(), text=products_wsdl)
            requests_mock.post(method_url, **kwargs)

        return _mock_product_method

    @pytest.fixture
    def file_fixture(self):
        def get_file(*args):
            path = self.FIXTURES_DIR.joinpath(*args)
            with open(str(path), "r") as f:
                return f.read()

        return get_file
