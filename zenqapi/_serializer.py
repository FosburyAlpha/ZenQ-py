from typing import Union
from tickers import dct_all_ticker_info, Ticker


def from_textual_order_type_to_integer_order_type(apiOrderType: Union[str, int]) -> int:
    apiOrderTypeDecoded: int = 0
    if isinstance(apiOrderType, str):
        if apiOrderType.lower() == 'buy':
            apiOrderTypeDecoded = 1
        elif apiOrderType.lower() == 'sell':
            apiOrderTypeDecoded = -1
        else:
            apiOrderTypeDecoded = 0
    else:
        apiOrderTypeDecoded = apiOrderType
    return apiOrderTypeDecoded


def from_ticker_id_or_obj_to_ticker_name(symbol: Union[str, int, Ticker]) -> str:
    symbolDecoded = symbol
    a = dct_all_ticker_info
    if isinstance(symbol, int):
        symbolDecoded = dct_all_ticker_info.get(symbol, "")
        if symbolDecoded != "":
            symbolDecoded = symbolDecoded.ticker_name
    if isinstance(symbol, Ticker):
        symbolDecoded = dct_all_ticker_info.get(symbol.ticker_id, "")
        if symbolDecoded != "":
            symbolDecoded = symbolDecoded.ticker_name
    return symbolDecoded


def from_tickert_id_to_ticker_name_with_usdt_suffix(symbol: Union[str, int]) -> str:
    symbolDecoded = symbol
    if isinstance(symbol, int):
        symbolDecoded = dct_all_ticker_info.get(symbol, "")
        if symbolDecoded != "":
            symbolDecoded = symbolDecoded.ticker_name
    return symbolDecoded


def from_ticker_name_or_obj_to_ticker_id(symbol: Union[str, int, Ticker]) -> int:
    symbolDecoded = symbol
    if isinstance(symbol, str):
        symbolDecoded = dct_all_ticker_info.get(symbol, -1)
        if symbolDecoded != -1:
            symbolDecoded = symbolDecoded.ticker_id
    if isinstance(symbol, Ticker):
        symbolDecoded = symbol.ticker_id
    return symbolDecoded
