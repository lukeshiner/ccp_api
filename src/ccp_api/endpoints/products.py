"""The products endpoint for the Cloud Commerce Pro API."""

import zeep
from ccp_api import exceptions

from ..endpoint import Endpoint, _Method


class Products(Endpoint):
    """Endpoint for managing Cloud Commerce Pro products."""

    ENDPOINT = "CCPApiProductsService"

    def get_active_sales_channels(self):
        """Return information about active sales channels.

        Returns:
            TODO

        Raises:
            ccp_api.exceptions.ResponseError: If the API call response contains an error
                message.

        """
        return _GetActiveSalesChannels(self).call()

    def get_product_by_barcode(self, barcode):
        """Find a product by it's barcode.

        Args:
            barcode(str): The barcode of the product to be found.

        Returns:
            :obj:`zeep.objects.APIProduct` or None:

            If a product with the given barcode exists it will be returned as
            :obj:`zeep.objects.APIProduct`, otherwise None will be returned.

        Raises:
            ccp_api.exceptions.ResponseError: If the API call response contains an error
                message.

        """
        return _GetProductByBarcode(self).call(barcode)

    def get_product_by_ID(self, product_id):
        """Find a product by it's product ID.

        Args:
            barcode(str): The product ID of the product to be found.

        Returns:
            :obj:`zeep.objects.APIProduct` or None:

            If a product with the given barcode exists it will be returned as
            :obj:`zeep.objects.APIProduct`, otherwise None will be returned.

        Raises:
            ccp_api.exceptions.ResponseError: If the API call response contains an error
                message.

        """
        return _GetProductByID(self).call(product_id)

    def get_product_by_SKU(self, sku):
        """Find a product by it's SKU.

        Args:
            barcode(str): The SKU of the product to be found.

        Returns:
            :obj:`zeep.objects.APIProduct` or None:

            If a product with the given barcode exists it will be returned as
            :obj:`zeep.objects.APIProduct`, otherwise None will be returned.

        Raises:
            ccp_api.exceptions.ResponseError: If the API call response contains an error
                message.

        """
        return _GetProductBySKU(self).call(sku)

    def get_product_images(self, product_id):
        """Return information about the images associated with a product.

        Args:
            product_id(str): The ID of the product for which to return image information.

        Returns:
            TODO

        Raises:
            ccp_api.exceptions.ResponseError: If the API call response contains an error
                message.

        """
        return _GetProductImages(self).call(product_id)

    def set_external_product_ID(self, api_product, external_product_id):
        """Set the external product ID of a product.

        Args:
            api_product (:obj:`zeep.objects.APIProduct`): A representation of the product
                to be altered, as returned by `ccp_api.products.get_product_by_ID`.

            external_product_id (str): The new external product ID to set.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            ccp_api.exceptions.ResponseError: If the API call response contains an error
                message.

        """
        return _SetExternalProductID(self).call(api_product, external_product_id)


class _GetProductByID(_Method):
    method_name = "getProductByID"

    def handle_request_exception(self, e):
        if isinstance(e, zeep.exceptions.Fault):
            raise exceptions.ResponseError("Product not found")


class _GetProductBySKU(_Method):
    method_name = "getProductByManufacturerSKU"

    def process_response(self, response):
        if response.Content.ID == 0:
            return None
        else:
            return response.Content


class _GetProductByBarcode(_Method):
    method_name = "getProductByBarcode"

    def process_response(self, response):
        if response.Content.ID == 0:
            return None
        else:
            return response.Content


class _GetActiveSalesChannels(_Method):
    method_name = "getActiveSalesChannels"

    def process_response(self, response):
        return response.Content.APISalesChannel


class _GetProductImages(_Method):
    method_name = "getProductImages"

    def process_response(self, response):
        if response.Content is None:
            return []
        else:
            return response.Content.APIProductImage


class _SetExternalProductID(_Method):
    method_name = "setExternalProductId"

    def process_content(self, api_product, external_product_id):
        api_product.ExternalProductId = external_product_id
        return api_product


products = Products()
