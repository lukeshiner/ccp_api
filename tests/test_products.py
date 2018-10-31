import ccp_api
import pytest

from .test_ccp_api import Base_ccp_api_Test


class TestProducts(Base_ccp_api_Test):
    @pytest.fixture
    def products_wsdl(self, file_fixture):
        return file_fixture("products", "wsdl.xml")

    @pytest.fixture
    def product_by_ID_response(self, file_fixture):
        return file_fixture("products", "get_product_by_ID_response.xml")

    @pytest.fixture
    def get_product_by_ID_failed_response(self, file_fixture):
        return file_fixture("products", "get_product_by_ID_failed_response.xml")

    @pytest.fixture
    def product_by_SKU_response(self, file_fixture):
        return file_fixture("products", "get_product_by_SKU_response.xml")

    @pytest.fixture
    def get_product_by_SKU_empty_response(self, file_fixture):
        return file_fixture("products", "get_product_by_SKU_empty_response.xml")

    @pytest.fixture
    def product_by_barcode_response(self, file_fixture):
        return file_fixture("products", "get_product_by_barcode_response.xml")

    @pytest.fixture
    def get_products_by_barcode_empty_response(self, file_fixture):
        return file_fixture("products", "get_products_by_barcode_empty_response.xml")

    @pytest.fixture
    def get_active_sales_channels_response(self, file_fixture):
        return file_fixture("products", "get_active_sales_channels_response.xml")

    @pytest.fixture
    def get_product_images_response(self, file_fixture):
        return file_fixture("products", "get_product_images_response.xml")

    @pytest.fixture
    def set_external_product_ID_response(self, file_fixture):
        return file_fixture("products", "set_external_product_ID_response.xml")


class Test_get_product_by_ID(TestProducts):
    def test_product_by_ID_returns_a_product(
        self, mock_product_method, product_by_ID_response
    ):
        mock_product_method(text=product_by_ID_response)
        response = ccp_api.products.get_product_by_ID("1234864")
        assert response.Name == "Ladies Hooded Cotton Terry Towelling Robe"

    def test_get_product_by_ID_raises_when_no_product_matches(
        self, mock_product_method, get_product_by_ID_failed_response
    ):
        mock_product_method(text=get_product_by_ID_failed_response, status_code=500)
        with pytest.raises(ccp_api.exceptions.ResponseError):
            ccp_api.products.get_product_by_ID("1234864")


class Test_get_product_by_SKU(TestProducts):
    def test_product_by_SKU_returns_a_product(
        self, mock_product_method, product_by_SKU_response
    ):
        mock_product_method(text=product_by_SKU_response)
        response = ccp_api.products.get_product_by_SKU("ABC_DEF_GHI")
        assert response.Name == "Ladies Hooded Cotton Terry Towelling Robe"

    def test_get_product_by_SKU_returns_None_when_no_match_is_found(
        self, mock_product_method, get_product_by_SKU_empty_response
    ):
        mock_product_method(text=get_product_by_SKU_empty_response)
        response = ccp_api.products.get_product_by_SKU("ABC_DEF_GHI")
        assert response is None


class Test_get_product_by_barcode(TestProducts):
    def test_product_by_barcode_returns_a_product(
        self, mock_product_method, product_by_barcode_response
    ):
        mock_product_method(text=product_by_barcode_response)
        response = ccp_api.products.get_product_by_barcode("7106544676954")
        assert response.Name == "Ladies Hooded Cotton Terry Towelling Robe"

    def test_get_product_by_barcode_returns_None_when_no_match_is_found(
        self, mock_product_method, get_products_by_barcode_empty_response
    ):
        mock_product_method(text=get_products_by_barcode_empty_response)
        response = ccp_api.products.get_product_by_barcode("7106544676954")
        assert response is None


class Test_get_product_by_get_active_sales_channels(TestProducts):
    def test_get_active_sales_channels_returns_sales_channels_information(
        self, mock_product_method, get_active_sales_channels_response
    ):
        mock_product_method(text=get_active_sales_channels_response)
        response = ccp_api.products.get_active_sales_channels()
        assert response[0].ID == 3541


class Test_get_product_images(TestProducts):
    def test_get_product_images_returns_product_image_information(
        self, mock_product_method, get_product_images_response
    ):
        mock_product_method(text=get_product_images_response)
        response = ccp_api.products.get_product_images("1234864")
        assert response[0].ID == 14601918


class Test_set_external_product_id(TestProducts):
    def test_set_external_product_id(
        self,
        mock_product_method,
        product_by_ID_response,
        set_external_product_ID_response,
    ):
        mock_product_method(text=product_by_ID_response)
        product = ccp_api.products.get_product_by_ID("1234864")
        mock_product_method(text=set_external_product_ID_response)
        response = ccp_api.products.set_external_product_ID(product, "a001")
        assert response is True
