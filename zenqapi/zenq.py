import json
import requests
from _config import *
from _serializer import *
from _utils import filter_order
from .signatures.response import APIStandardResponse, APIUserBalances


class Client:
    def __init__(self, apiKey: str, apiSecret: str, test: bool = True):
        """
        Initializes the client to communicate with the Zenq exchange.

        :param apiKey: The API key associated with the user account, generated from the Zenq exchange.
        :param apiSecret: The API secret key associated with the user account, generated from the Zenq exchange.
        :param test: A flag to indicate the environment. 
                     Set to True for Paper Money (test environment) or False for Real Money (live trading).

        """

        self.apiKey = apiKey
        self.apiSecret = apiSecret
        if test:
            self.base_url = test_url
        else:
            self.base_url = prod_url

    def place_limit_order(self, apiQuantity: float, apiOrderType: Union[int, str], apiPrice: float, apiTickerId: Union[int, str, Ticker]) -> APIStandardResponse:
        """
        Place a limit order on the exchange.

        :param apiQuantity: The quantity to order, expressed in base token units.
        :param apiOrderType: The type of the order. 
                             Can be a string with the value "buy" or "sell",or an integer (1 for "buy" or -1 for "sell").
        :param apiPrice: The price level at which the order is placed.
        :param apiTickerId: The market pair identifier. 
                            This can either be a string (e.g., "BTCUSDT") or the ticker ID from the Zenq exchange.
        :return: APIStandardResponse Object with this property:
             status_code: The raw status code of server response.
             order_id: The order_id code from server response if valorized otherwise is 0.
             message: The message of server response, it contains the content, also errors.
             is_error: A flag that is True if the call returned a not 2XX code.
        """

        apiOrderTypeDecoded = from_textual_order_type_to_integer_order_type(apiOrderType)
        if apiOrderTypeDecoded == 0:
            return APIStandardResponse(status_code="R422", message="apiOrderType must be a valid value", is_error=True)

        symbolDecoded = from_ticker_name_or_obj_to_ticker_id(apiTickerId)
        if symbolDecoded == -1:
            return APIStandardResponse(status_code="R422", message="Ticker name not found into library.", is_error=True)

        params = {
            "apiKeyID": self.apiKey,
            "apiKeyPassword": self.apiSecret,
            "apiQuantity": apiQuantity,
            "apiOrderType": apiOrderTypeDecoded,
            "apiPrice": apiPrice,
            "apiTickerId": symbolDecoded,
            "outputType": "json"
        }
        url = f"{self.base_url}{place_order_url}"
        response = requests.get(url, params=params)
        content = json.loads(response.content.decode('utf-8'))

        return APIStandardResponse.from_dict(content)

    def place_market_order(self, apiQuantity: float, apiOrderType: Union[int, str], apiTickerId: [int, str, Ticker]) -> APIStandardResponse:
        """
        Place a market order on the exchange.

        :param apiQuantity: The quantity to order, expressed in base token units.
        :param apiOrderType: The type of the order. 
                             Can be a string with the value "buy" or "sell", or an integer (1 for "buy" or -1 for "sell").
        :param apiTickerId: The market pair identifier. 
                            This can either be a string (e.g., "BTCUSDT") or the ticker ID from the Zenq exchange.
        :return: APIStandardResponse Object with this property:
             status_code: The raw status code of server response.
             order_id: The order_id code from server response if valorized otherwise is 0.
             message: The message of server response, it contains the content, also errors.
             is_error: A flag that is True if the call returned a not 2XX code.
        """

        apiOrderTypeDecoded = from_textual_order_type_to_integer_order_type(apiOrderType)
        if apiOrderTypeDecoded == 0:
            return APIStandardResponse(status_code="R422", message="apiOrderType must be a valid value", is_error=True)

        symbolDecoded = from_ticker_name_or_obj_to_ticker_id(apiTickerId)
        if symbolDecoded == -1:
            return APIStandardResponse(status_code="R422", message="Ticker name not found into library.", is_error=True)

        params = {
            "apiKeyID": self.apiKey,
            "apiKeyPassword": self.apiSecret,
            "apiQuantity": apiQuantity,
            "apiOrderType": apiOrderTypeDecoded,
            "apiTickerId": symbolDecoded,
            "outputType": "json"
        }
        url = f"{self.base_url}{place_order_url}"
        response = requests.get(url, params=params)
        content = json.loads(response.content.decode('utf-8'))

        return APIStandardResponse.from_place_order_market_dict(content)

    def search_ticker(self, symbol: Union[int, str]) -> APIStandardResponse:
        """
        Retrieve information about a specific symbol, either by its string representation (e.g., "BTC") or its ID.
        
        :param symbol: The symbol to search. 
                       This can be a string, the ticker ID from the Zenq exchange, or the ticker Object from library.
                       E.g. ADAUSDC, "ADAUSDC", 40895, ADAUSDC.ticker_id
        :return: APIStandardResponse Object with this property:
             status_code: The raw status code of server response.
             order_id: The order_id code from server response if valorized otherwise is 0.
             message: The message of server response, it contains the content, also errors.
             is_error: A flag that is True if the call returned a not 2XX code.
        """

        symbolDecoded = from_ticker_id_or_obj_to_ticker_name(symbol)
        if symbolDecoded == "":
            return APIStandardResponse(status_code="R422", message="Ticker name not found into library.", is_error=True)
        params = {
            "apiKeyID": self.apiKey,
            "apiKeyPassword": self.apiSecret,
            "st": symbolDecoded,
            "outputType": "json"
        }
        url = f"{self.base_url}{search_ticker_url}"
        response = requests.get(url, params=params)
        content = json.loads(response.content.decode('utf-8'))
        print(url)

        return APIStandardResponse.from_search_ticker_dict(content)

    def order_list(self, apiTickerId: Union[int, str, Ticker] = "", orderId: str = ""):
        """
        Retrieve a filtered list of orders, optionally filtering by ticker ID or order ID.
        
        :param apiTickerId: The ticker ID to filter orders by. If left empty, no filtering is applied based on the ticker.
                            This can either be a string (e.g., "BTCUSDT") or the ticker ID from the Zenq exchange.
        :param orderId: The specific order ID to filter by. If left empty, no filtering is applied based on the order ID.
        :return: APIStandardResponse Object with this property:
             status_code: The raw status code of server response.
             order_id: The order_id code from server response if valorized otherwise is 0.
             message: The message of server response, it contains the content, also errors.
             is_error: A flag that is True if the call returned a not 2XX code.
        """
        params = {
            "apiKeyID": self.apiKey,
            "apiKeyPassword": self.apiSecret,
            "outputType": "json"
        }
        url = f"{self.base_url}{order_list_url}"
        response = requests.get(url, params=params)
        content = json.loads(response.content.decode('utf-8'))

        apiTickerNameDecoded = ""
        if apiTickerId != "":
            apiTickerNameDecoded = from_ticker_id_or_obj_to_ticker_name(apiTickerId)
            if apiTickerNameDecoded == "":
                return APIStandardResponse(status_code="R422", message="Ticker name not found into library.", is_error=True)

        filtered_content = filter_order(content, apiTickerNameDecoded, orderId)

        return APIStandardResponse.from_order_list_dict(filtered_content)

    def order_modify(self, orderId: str, newPrice: float, newQuantity: float, marketValue: float, apiTickerId: Union[int, str, Ticker] = 0) -> APIStandardResponse:
        # {"code":"R200","data":{"orderId":"48485","message":"Order was placed successfully. Order #  48485. \u003Cbr\u003EBTCUSDT X 0.00010 @ 125213.000"},"errors":[],"extra":[]}
        # {"success":1,"message":"Success: Modify order has been done\r\n"}
        """
        Modify an existing order by updating its price and quantity.

        :param orderId: The unique identifier of the order to be modified.
        :param newPrice: The new price for the order.
        :param newQuantity: The new quantity for the order.
        :param marketValue: The current market value used to validate the modification.
        :param apiTickerId: The ticker ID. If left empty, no filtering is applied based on the ticker.
                            This can either be a string (e.g., "BTCUSDT") or the ticker ID from the Zenq exchange.
        :return: APIStandardResponse Object with this property:
             status_code: The raw status code of server response.
             order_id: The order_id code from server response if valorized otherwise is 0.
             message: The message of server response, it contains the content, also errors.
             is_error: A flag that is True if the call returned a not 2XX code.
        """

        symbolDecoded = from_ticker_name_or_obj_to_ticker_id(apiTickerId)
        if symbolDecoded == -1:
            return APIStandardResponse(status_code="R422", message="Ticker name not found into library.", is_error=True)

        params = {
            "orderId": orderId,
            "newPrice": newPrice,
            "newQuantity": newQuantity,
            "marketValue": marketValue,
            "apiTickerId": symbolDecoded,
            "apiKeyID": self.apiKey,
            "apiKeyPassword": self.apiSecret,
            "outputType": "json"
        }
        url = f"{self.base_url}{modify_order_url}"
        response = requests.get(url, params=params)
        return APIStandardResponse.from_modify_order(response=response, status_code=response.status_code,
                                                     order_id=orderId)

    def order_cancel(self, orderId: str, apiTickerId: Union[int, str, Ticker] = "") -> APIStandardResponse:
        # {"code":"R200","data":{"orderId":"48485","message":"Order was placed successfully. Order #  48485. \u003Cbr\u003EBTCUSDT X 0.00010 @ 125213.000"},"errors":[],"extra":[]}
        # Success: Order #48484 has been cancelled successfully
        """
        Cancel an existing order on the exchange.

        :param orderId: The unique identifier of the order to be canceled.
        :param apiTickerId: The ticker ID. If left empty, no filtering is applied based on the ticker.
                            This can either be a string (e.g., "BTCUSDT") or the ticker ID from the Zenq exchange.
        :return: APIStandardResponse Object with this property:
             status_code: The raw status code of server response.
             order_id: The order_id code from server response if valorized otherwise is 0.
             message: The message of server response, it contains the content, also errors.
             is_error: A flag that is True if the call returned a not 2XX code.
        """
        orderId = int(orderId)

        symbolDecoded = from_ticker_name_or_obj_to_ticker_id(apiTickerId)
        if symbolDecoded == -1:
            return APIStandardResponse(status_code="R422", message="Ticker name not found into library.", is_error=True)

        params = {
            "orderId": orderId,
            "mode": 'modify',
            "apiTickerId": apiTickerId,
            "apiKeyID": self.apiKey,
            "apiKeyPassword": self.apiSecret,
            "outputType": "json"
        }

        url = f"{self.base_url}{cancel_order_url}"
        response = requests.get(url, params=params)
        return APIStandardResponse.from_cancel_order(response=response, status_code=response.status_code, order_id=str(orderId))

    def user_balances(self, userId: str = "") -> APIUserBalances:
        """
        Retrieve the balances of a user account.

        :param userId: (Optional) The unique identifier of the user.
                        If not provided, the balances for the current API key are retrieved.
        :return: #  TO DO
        """

        params = {
            "apiKeyID": self.apiKey,
            "apiKeyPassword": self.apiSecret,
            "outputType": "json"
        }

        if userId != "":
            params["userId"] = userId

        url = f"{self.base_url}{user_balances_url}"
        response = requests.get(url, params=params)
        content = json.loads(response.content.decode('utf-8'))
        return APIUserBalances.from_user_balance(data=content)
