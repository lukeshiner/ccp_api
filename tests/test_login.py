from pathlib import Path

import ccp_api
import pytest

from .base_tests import Base_ccp_api_Test


class TestCredentials(Base_ccp_api_Test):
    """Tests for API credential management."""

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def setup_method(cls):
        ccp_api.login.reset()

    @classmethod
    def teardown_method(cls):
        ccp_api.login.reset()

    def test_login(self):
        assert ccp_api.login.brand_id is None
        assert ccp_api.login.security_hash is None
        ccp_api.login.set(
            brand_id=self.TEST_BRAND_ID, security_hash=self.TEST_SECURITY_HASH
        )
        assert ccp_api.login.brand_id == self.TEST_BRAND_ID
        assert ccp_api.login.security_hash == self.TEST_SECURITY_HASH

    def test_get_credentials_fails_when_no_file_is_present(self, tmp_cwd):
        with pytest.raises(Exception):
            ccp_api.login.set()

    def test_loading_credentials_from_file(self, config_file):
        assert ccp_api.login.brand_id is None
        assert ccp_api.login.security_hash is None
        ccp_api.login.set()
        assert ccp_api.login.brand_id == self.TEST_BRAND_ID
        assert ccp_api.login.security_hash == self.TEST_SECURITY_HASH

    def test_exception_is_raised_when_config_file_is_malformed(self, tmp_cwd):
        filename = ccp_api.credentials.CredentialsFile.CREDENTIALS_FILE_NAME
        with open(filename, "w") as f:
            f.write("some text")
        with pytest.raises(Exception):
            ccp_api.login.set()

    def test_CredentialsFile_returns_path_to_config_file(self, config_file):
        returned_value = ccp_api.credentials.CredentialsFile().find()
        expected_path = Path.cwd().joinpath(
            ccp_api.credentials.CredentialsFile.CREDENTIALS_FILE_NAME
        )
        assert isinstance(returned_value, Path)
        assert str(returned_value) == str(expected_path)

    def test_CredentialsFile_find_method_reutrns_None_when_no_file_is_found(
        self, tmp_cwd
    ):
        assert ccp_api.credentials.CredentialsFile().find() is None

    def test_the_login_set_method_overrides_the_config_file(self, config_file):
        temp_brand_id = "999"
        temp_security_hash = "5,11"
        ccp_api.login.set(brand_id="999", security_hash="5,11")
        assert ccp_api.login.brand_id == temp_brand_id
        assert ccp_api.login.security_hash == temp_security_hash

    def test_exception_is_raised_when_makeing_a_request_with_no_credentials(self):
        assert ccp_api.login.brand_id is None
        assert ccp_api.login.security_hash is None
        with pytest.raises(ValueError):
            ccp_api.products.get_product_by_ID("1234864")
