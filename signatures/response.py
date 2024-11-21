import json
from typing import Optional, Dict, Any

import requests


class APIStandardResponse:
    """Class implementing the unified API response for REST API."""

    def __init__(self, status_code: str, order_id: Optional[str] = "", message: Optional[str] = "",
                 is_error: bool = False):
        """
        The init class for unified response.

        :param status_code: The raw status code of server response.
        :param order_id: The order_id code from server response if valorized otherwise is 0.
        :param message: The message of server response, it contains the content, also errors.
        :param is_error: A flag that is True if the call returned a not 2XX code.
        """
        self.status_code: str = status_code
        self.order_id: Optional[str] = order_id
        self.message: Optional[str] = message
        self.is_error: bool = is_error

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "APIStandardResponse":
        """Create an APIStandardResponse object from a dictionary."""

        status_code = data.get('code', '')

        if status_code == 'R403':
            error = data.get('errors', [])
            order_id = ''
            message = error[0]
            is_error = True
        else:
            content = data.get('data', [])
            if content != []:
                order_id = content.get('orderId', '')
                message = content.get('message', '')
                is_error = False
            else:
                error = data.get('errors', [])
                order_id = error.get('orderId', '')
                message = error.get('message', '')
                is_error = True

        return cls(
            status_code=status_code,
            order_id=order_id,
            message=message,
            is_error=is_error
        )

    @classmethod
    def from_search_ticker_dict(cls, data: Dict[str, Any]) -> "APIStandardResponse":
        """Create an APIStandardResponse object from a dictionary."""

        status_code = data.get('code', '')
        if status_code == 'R403':
            error = data.get('errors', [])
            message = error[0]
            is_error = True
        else:
            content = data.get('data', [])
            if content != []:
                message = content[0]
                is_error = False
            else:
                message = data.get('errors', "")
                if message == []:
                    message = "Ticker not found."
                is_error = True

        return cls(
            status_code=status_code,
            order_id='0',
            message=message,
            is_error=is_error
        )

    @classmethod
    def from_place_order_market_dict(cls, data: Dict[str, Any]) -> "APIStandardResponse":
        """Create an APIStandardResponse object from a dictionary."""

        status_code = data.get('code', '')

        content = data.get('data', [])
        if content != []:
            order_id = content.get('orderId', '')
            message = content.get('message', '')
            is_error = False
        else:
            error = data.get('errors', [])
            order_id = error.get('orderId', '')
            message = error.get('message', '')
            is_error = True

        return cls(
            status_code=status_code,
            order_id=order_id,
            message=message,
            is_error=is_error
        )

    @classmethod
    def from_order_list_dict(cls, data: Dict[str, Any]) -> "APIStandardResponse":
        """Create an APIStandardResponse object from a dictionary."""
        if not isinstance(data, list):
            status_code = data.get('code', '')

            content = data.get('data', [])
            if content != []:
                order_id = ''
                message = content
                is_error = False
            else:
                error = data.get('errors', [])
                order_id = ''
                message = error[0]
                is_error = True

            return cls(
                status_code=status_code,
                order_id=order_id,
                message=message,
                is_error=is_error
            )
        else:

            return cls(
                status_code="R200",
                order_id="0",
                message=str(data),
                is_error=False
            )

    @classmethod
    def from_modify_order(cls, response: requests.Response, status_code: int, order_id: str) -> "APIStandardResponse":
        """Create an APIStandardResponse object from a dictionary."""

        if 200 <= status_code < 300:
            response_content: dict = json.loads(response.content.decode('utf-8'))
            message = response_content.get('message', '')
            is_error = False
        else:

            error_content: str = response.content.decode('utf-8')
            if 'Order' not in error_content:
                errors: list = json.loads(error_content).get('errors', [])
                if errors != []:
                    message: str = errors[0]
                else:
                    raise Exception("Unable to catch error.")
            else:
                message: str = response.content.decode('utf-8')
            is_error = True

        return cls(
            status_code=str(status_code),
            order_id=order_id,
            message=message,
            is_error=is_error
        )

    @classmethod
    def from_cancel_order(cls, response: requests.Response, status_code: int, order_id: str) -> "APIStandardResponse":
        """Create an APIStandardResponse object from a dictionary."""

        if 200 <= status_code < 300:
            message = response.content.decode('utf-8')
            is_error = False
        else:
            try:
                error_content: str = response.content.decode('utf-8')
                if 'Order' not in error_content:
                    errors: list = json.loads(error_content).get('errors', [])
                    if errors != []:
                        message: str = errors[0]
                    else:
                        raise Exception("Unable to catch error.")
                else:
                    message: str = response.content.decode('utf-8')
            except BaseException as e:
                message = e
            is_error = True

        return cls(
            status_code=str(status_code),
            order_id=order_id,
            message=message,
            is_error=is_error
        )


class APIUserBalances:
    """Class implementing the unified API response for REST API of user balances."""

    def __init__(self, status_code: str, customerId: Optional[str] = "",
                 Balances: Optional[str] = "",
                 Positions: Optional[str] = "",
                 Equity: Optional[str] = "",
                 Totals: Optional[str] = "",
                 TotalBySecurityType: Optional[str] = "",
                 error: Optional[str] = "",
                 is_error: bool = False):
        """
        Standard response from user balances api.

        :param status_code: The raw status code of server response.
        :param customerId: The unique identifier for the customer associated with the response.
        :param Balances: A detailed representation of the user's account balances.
        :param Positions: Information about the user's open positions in various instruments or assets.
        :param Equity: The user's total equity, representing the value of all assets minus liabilities.
        :param Totals: Aggregated financial data, summarizing key metrics such as balances and equity.
        :param TotalBySecurityType: Breakdown of totals categorized by security type (e.g., stocks, bonds).
        :param error: Error details or messages, if any, returned by the API.
        :param is_error: A flag that is True if the call returned a not 2XX code.
        """

        self.status_code: str = status_code
        self.customerId: Optional[str] = customerId
        self.Balances: Optional[str] = Balances
        self.Positions: Optional[str] = Positions
        self.Equity: Optional[str] = Equity
        self.Totals: Optional[str] = Totals
        self.TotalBySecurityType: Optional[str] = TotalBySecurityType
        self.error: Optional[str] = error
        self.is_error: bool = is_error

    @classmethod
    def from_user_balance(cls, data: Dict[str, Any]) -> "APIUserBalances":
        """Create an APIStandardResponse object from a dictionary."""
        # b'{"code":"R200","data":{"customerId":"1000431","Balances":[{"currencySymbol":"USDT","precision":"2","cashBalance":"950.00","cashBalanceInLocalLocalCurrency":"902.78","availableForTrading":"950.00","availableForTradingLocalCurrency":"902.78","availableForWithdrawal":"950.00","availableForWithdrawalLocalCurrency":"902.78","localCurrencySymbol":"EUR","reserved":"0","reservedLocalCurrency":"0","currencyDesc":"USDT","suspendedCurrency":"0","currencyId":"1463","portfolioValue":"0","allowMargin":"1","isMinorCurrency":"0","minorToNormalRatio":"1.0","overdraft":"0.00","marginExposure":"0","exchangeRateUSD":"1","currencylogourl":"\\/images\\/currencies\\/USDT.PNG","AVGCost_DefaultCurrency":"0","DefaultCurrencyRatio":"1.00","UnRealized_DefaultCurrency":"0","SoldValue_DefaultCurrency":"0","RealizedPL_DefaultCurrency":"0"},{"currencySymbol":"USDT-ZENQ","precision":"2","cashBalance":"26022.93","cashBalanceInLocalLocalCurrency":"24729.57","availableForTrading":"26022.93","availableForTradingLocalCurrency":"24729.57","availableForWithdrawal":"26022.93","availableForWithdrawalLocalCurrency":"24729.57","localCurrencySymbol":"EUR","reserved":"0","reservedLocalCurrency":"0","currencyDesc":"USDT-ZENQ","suspendedCurrency":"0","currencyId":"1778","portfolioValue":"0","allowMargin":"1","isMinorCurrency":"0","minorToNormalRatio":"1.0","overdraft":"0.00","marginExposure":"0","exchangeRateUSD":"1","currencylogourl":"\\/images\\/currencies\\/USDT.PNG","AVGCost_DefaultCurrency":"0","DefaultCurrencyRatio":"1.00","UnRealized_DefaultCurrency":"0","SoldValue_DefaultCurrency":"0","RealizedPL_DefaultCurrency":"0"},{"currencySymbol":"BTC-ZENQ","precision":"8","cashBalance":"1.02374919","cashBalanceInLocalLocalCurrency":"89969.87","availableForTrading":"1.02374919","availableForTradingLocalCurrency":"89969.87292157","availableForWithdrawal":"1.02374919","availableForWithdrawalLocalCurrency":"89969.87","localCurrencySymbol":"EUR","reserved":"0","reservedLocalCurrency":"0","currencyDesc":"BTC-ZENQ","suspendedCurrency":"0","currencyId":"1779","portfolioValue":"0","allowMargin":"1","isMinorCurrency":"0","minorToNormalRatio":"1.0","overdraft":"0.00000000","marginExposure":"0","exchangeRateUSD":"1.0813289E-5","currencylogourl":"\\/images\\/currencies\\/BTC.PNG","AVGCost_DefaultCurrency":"0","DefaultCurrencyRatio":"1.00","UnRealized_DefaultCurrency":"0","SoldValue_DefaultCurrency":"0","RealizedPL_DefaultCurrency":"0"}],"Positions":[{"symbol":"BTCUSDT","PortfolioWeight":"0","marketSymbol":"Binance","currencySymbol":"USDT-Binance","quantity":"1.02788","lastPrice":"88519.53000000","lastDelta":"251.67","deltaPercent":"0.28512","totalMarketValue":"90987.4544964","totalMarketValueInDefault":"0","averageCost":"71970.58895273","securityType":"Crypto Asset","CustodianID":"0","subUserId":"0","priceDecimal":"3","marketId":"118","contractSize":"1","tickerId":"32777","reserved":"0","available":"1.02788","custodianName":"MKT","bep":"71970.58895273","idcSymbol":"","feedMarketSymbol":"","feedSource":"","isin":"","symbolID":"BTCUSDT","BloombergSymbol":"","DescriptionEN":"Bitcoin","DescriptionAR":"Bitcoin","lastBid":"88519.53000000","lastAsk":"88519.54000000","lastVolume":"4585156073","MarginPaid":"73977.128972733","totalCost":"73977.128972733","UnrealizedPL":"17010.325523668","UnrealizedPLInDefault":"16163.2848635358653880652","UnrealizedPLPercent":"22.99","AvgCostRealizedPLAdjusted":"71970.58895273","initialMargin":"0","securityTypeId":"16","bondMaturityDate":"1900-01-01","bondFaceValue":"100.0","bondDistributionPercent":"0.0","bondYieldPercent":"0","bondDistributionsPerYear":"0","QuantityDecimal":"8","CurrencyDecimals":"2","PendingQuantity":"0","FuturesOptionsExpiryDate":"1900-01-01","UnderlyingTickerID":"0","UnderlyingSymbol":"","OptionType":"","OptionStrikePrice":"0.0","CryptoSymbolBought":"BTC","CryptoSymbolSold":"USDT","dayGainLocal":"245.80508745666","costLocal":"70293.387816718","marketValueLocal":"86456.672679592","realizedGainLocal":"1.0765814989346","accruedInterest":"0","bondRatingStandardAndPoors":"","accumulatedCoupon":"0","averageCostComm":"71970.58895273","actualCost":"73977.128972733","actualCostInDefault":"70293.3878195988618002187","plPercentage":"22.995564656122","bidYTM":"0.0","unrealizedGLComm":"17010.325523668","realizedPL":"1.133","PendingQuantityBuy":"0","PendingQuantitySell":"0","actualCostLocal":"70293.387816718","unrealizedPLLocal":"16163.284862873","symbolAlias":"BTCUSDT","symbolAlias2":"BTC","dayGain":"258.6865596","subUserNameEN":"Main","lastPrevPrice":"88267.86","priceCurrencySymbol":"USDT-Binance","unrealizedPL_NoPLAdded":"17010.325523668","unrealizedPLUSD":"17008.624661202","marketValueUSD":"90978.356660734","takeProfitAmount":"0","takeProfitStr":"","takeProfitQty":"0","stopLossAmount":"0","stopLossStr":"","stopLossQty":"0","hasTrigger":"0","BondNextDistributionDate":"1900-01-01","marginRequiredPercent":0}],"Equity":[{"EquityValue":"115602.04","MarginRatio":"%100.00","CurrencySymbol":"EUR","requiredDeposit":0,"requiredSelling":0,"CurrencyDecimals":"2"}],"Totals":[{"TotalCost":"0.00","TotalMarketValue":"0.00","TotalGainLoss":"16163.28","TotalMarginRequired":"70293.39","CurrencySymbol":"EUR","CurrencyDecimals":"2","NonCashMarginRationPercent":"0.00","DailyUnrealizedPnL":"245.81","DailyUnrealizedPnLPercent":"0.21","DailyRealizedPnL":"","DailyRealizedPnLPercent":"","DailyTotalPnL":"","DailyTotalPnLPercent":"","CurrencyDecimalsPreferred":"2"}],"TotalBySecurityType":[{"SecurityType":"Crypto Asset","TotalMarketValueLocalCurrency":"86456.672679592","CurrencyDecimalLocal":"2","TotalMarketValueUSD":"90978.356660734","UnrealizedPLLocal":"16163.284862873","UnrealizedPLUSD":"17008.624661202","CurrencyDecimalUSD":"2","SecurityTypeID":"16"}]},"errors":[],"extra":[]}'
        # con filtro b'{"code":"R200","data":{"customerId":"1000431","Balances":[{"currencySymbol":"USDT","precision":"2","cashBalance":"950.00","cashBalanceInLocalLocalCurrency":"899.62","availableForTrading":"950.00","availableForTradingLocalCurrency":"899.62","availableForWithdrawal":"950.00","availableForWithdrawalLocalCurrency":"899.62","localCurrencySymbol":"EUR","reserved":"0","reservedLocalCurrency":"0","currencyDesc":"USDT","suspendedCurrency":"0","currencyId":"1463","portfolioValue":"0","allowMargin":"1","isMinorCurrency":"0","minorToNormalRatio":"1.0","overdraft":"0.00","marginExposure":"0","exchangeRateUSD":"1","currencylogourl":"\\/images\\/currencies\\/USDT.PNG","AVGCost_DefaultCurrency":"0","DefaultCurrencyRatio":"1.00","UnRealized_DefaultCurrency":"0","SoldValue_DefaultCurrency":"0","RealizedPL_DefaultCurrency":"0"},{"currencySymbol":"USDT-ZENQ","precision":"2","cashBalance":"26022.93","cashBalanceInLocalLocalCurrency":"24645.39","availableForTrading":"26022.93","availableForTradingLocalCurrency":"24645.39","availableForWithdrawal":"26022.93","availableForWithdrawalLocalCurrency":"24645.39","localCurrencySymbol":"EUR","reserved":"0","reservedLocalCurrency":"0","currencyDesc":"USDT-ZENQ","suspendedCurrency":"0","currencyId":"1778","portfolioValue":"0","allowMargin":"1","isMinorCurrency":"0","minorToNormalRatio":"1.0","overdraft":"0.00","marginExposure":"0","exchangeRateUSD":"0.9999","currencylogourl":"\\/images\\/currencies\\/USDT.PNG","AVGCost_DefaultCurrency":"0","DefaultCurrencyRatio":"1.00","UnRealized_DefaultCurrency":"0","SoldValue_DefaultCurrency":"0","RealizedPL_DefaultCurrency":"0"},{"currencySymbol":"BTC-ZENQ","precision":"8","cashBalance":"1.02374919","cashBalanceInLocalLocalCurrency":"89119.31","availableForTrading":"1.02374919","availableForTradingLocalCurrency":"89119.31246409","availableForWithdrawal":"1.02374919","availableForWithdrawalLocalCurrency":"89119.31","localCurrencySymbol":"EUR","reserved":"0","reservedLocalCurrency":"0","currencyDesc":"BTC-ZENQ","suspendedCurrency":"0","currencyId":"1779","portfolioValue":"0","allowMargin":"1","isMinorCurrency":"0","minorToNormalRatio":"1.0","overdraft":"0.00000000","marginExposure":"0","exchangeRateUSD":"1.08782275E-5","currencylogourl":"\\/images\\/currencies\\/BTC.PNG","AVGCost_DefaultCurrency":"0","DefaultCurrencyRatio":"1.00","UnRealized_DefaultCurrency":"0","SoldValue_DefaultCurrency":"0","RealizedPL_DefaultCurrency":"0"}],"Positions":[{"symbol":"BTCUSDT","PortfolioWeight":"0","marketSymbol":"ZENQ","currencySymbol":"USDT-Binance","quantity":"1.02788","lastPrice":"91909.95000000","lastDelta":"590.59","deltaPercent":"0.64673","totalMarketValue":"94472.399406","totalMarketValueInDefault":"0","averageCost":"71970.58895273","securityType":"Crypto Asset","CustodianID":"0","subUserId":"0","priceDecimal":"3","marketId":"118","contractSize":"1","tickerId":"32777","reserved":"0","available":"1.02788","custodianName":"MKT","bep":"71970.58895273","idcSymbol":"","feedMarketSymbol":"","feedSource":"","isin":"","symbolID":"BTCUSDT","BloombergSymbol":"","DescriptionEN":"Bitcoin","DescriptionAR":"Bitcoin","lastBid":"91909.95000000","lastAsk":"91909.96000000","lastVolume":"2304154466","MarginPaid":"73977.128972733","totalCost":"73977.128972733","UnrealizedPL":"20495.270433268","UnrealizedPLInDefault":"19410.2381217602857138008","UnrealizedPLPercent":"27.70","AvgCostRealizedPLAdjusted":"71970.58895273","initialMargin":"0","securityTypeId":"16","bondMaturityDate":"1900-01-01","bondFaceValue":"100.0","bondDistributionPercent":"0.0","bondYieldPercent":"0","bondDistributionsPerYear":"0","QuantityDecimal":"8","CurrencyDecimals":"2","PendingQuantity":"0","FuturesOptionsExpiryDate":"1900-01-01","UnderlyingTickerID":"0","UnderlyingSymbol":"","OptionType":"","OptionStrikePrice":"0.0","CryptoSymbolBought":"BTC","CryptoSymbolSold":"USDT","dayGainLocal":"574.86330416667","costLocal":"70054.099405997","marketValueLocal":"89462.4994375","realizedGainLocal":"1.0729166666667","accruedInterest":"0","bondRatingStandardAndPoors":"","accumulatedCoupon":"0","averageCostComm":"71970.58895273","actualCost":"73977.128972733","actualCostInDefault":"70060.7339434828292691798","plPercentage":"27.706405638995","bidYTM":"0.0","unrealizedGLComm":"20495.270433268","realizedPL":"1.133","PendingQuantityBuy":"0","PendingQuantitySell":"0","actualCostLocal":"70054.099405997","unrealizedPLLocal":"19408.400031503","symbolAlias":"BTCUSDT","symbolAlias2":"BTC","dayGain":"607.0556492","subUserNameEN":"Main","lastPrevPrice":"91319.36","priceCurrencySymbol":"USDT-Binance","unrealizedPL_NoPLAdded":"20495.270433268","unrealizedPLUSD":"20495.270433268","marketValueUSD":"94472.399406","takeProfitAmount":"0","takeProfitStr":"","takeProfitQty":"0","stopLossAmount":"0","stopLossStr":"","stopLossQty":"0","hasTrigger":"0","BondNextDistributionDate":"1900-01-01","marginRequiredPercent":0}],"Equity":[{"EquityValue":"114664.26","MarginRatio":"%100.00","CurrencySymbol":"EUR","requiredDeposit":0,"requiredSelling":0,"CurrencyDecimals":"2"}],"Totals":[{"TotalCost":"0.00","TotalMarketValue":"0.00","TotalGainLoss":"19408.40","TotalMarginRequired":"70060.73","CurrencySymbol":"EUR","CurrencyDecimals":"2","NonCashMarginRationPercent":"0.00","DailyUnrealizedPnL":"574.92","DailyUnrealizedPnLPercent":"0.50","DailyRealizedPnL":"","DailyRealizedPnLPercent":"","DailyTotalPnL":"","DailyTotalPnLPercent":"","CurrencyDecimalsPreferred":"2"}],"TotalBySecurityType":[{"SecurityType":"Crypto Asset","TotalMarketValueLocalCurrency":"89462.4994375","CurrencyDecimalLocal":"2","TotalMarketValueUSD":"94472.399406","UnrealizedPLLocal":"19408.400031503","UnrealizedPLUSD":"20495.270433268","CurrencyDecimalUSD":"2","SecurityTypeID":"16"}]},"errors":[],"extra":[]}'
        # b'{"code":"R200","data":{"customerId":"1000431","Balances":[{"currencySymbol":"USDT","precision":"2","cashBalance":"950.00","cashBalanceInLocalLocalCurrency":"899.28","availableForTrading":"950.00","availableForTradingLocalCurrency":"899.28","availableForWithdrawal":"950.00","availableForWithdrawalLocalCurrency":"899.28","localCurrencySymbol":"EUR","reserved":"0","reservedLocalCurrency":"0","currencyDesc":"USDT","suspendedCurrency":"0","currencyId":"1463","portfolioValue":"0","allowMargin":"1","isMinorCurrency":"0","minorToNormalRatio":"1.0","overdraft":"0.00","marginExposure":"0","exchangeRateUSD":"1","currencylogourl":"\\/images\\/currencies\\/USDT.PNG","AVGCost_DefaultCurrency":"0","DefaultCurrencyRatio":"1.00","UnRealized_DefaultCurrency":"0","SoldValue_DefaultCurrency":"0","RealizedPL_DefaultCurrency":"0"},{"currencySymbol":"USDT-ZENQ","precision":"2","cashBalance":"26022.93","cashBalanceInLocalLocalCurrency":"24636.06","availableForTrading":"26022.93","availableForTradingLocalCurrency":"24636.06","availableForWithdrawal":"26022.93","availableForWithdrawalLocalCurrency":"24636.06","localCurrencySymbol":"EUR","reserved":"0","reservedLocalCurrency":"0","currencyDesc":"USDT-ZENQ","suspendedCurrency":"0","currencyId":"1778","portfolioValue":"0","allowMargin":"1","isMinorCurrency":"0","minorToNormalRatio":"1.0","overdraft":"0.00","marginExposure":"0","exchangeRateUSD":"0.9999","currencylogourl":"\\/images\\/currencies\\/USDT.PNG","AVGCost_DefaultCurrency":"0","DefaultCurrencyRatio":"1.00","UnRealized_DefaultCurrency":"0","SoldValue_DefaultCurrency":"0","RealizedPL_DefaultCurrency":"0"},{"currencySymbol":"BTC-ZENQ","precision":"8","cashBalance":"1.02374919","cashBalanceInLocalLocalCurrency":"89250.62","availableForTrading":"1.02374919","availableForTradingLocalCurrency":"89250.61592782","availableForWithdrawal":"1.02374919","availableForWithdrawalLocalCurrency":"89250.62","localCurrencySymbol":"EUR","reserved":"0","reservedLocalCurrency":"0","currencyDesc":"BTC-ZENQ","suspendedCurrency":"0","currencyId":"1779","portfolioValue":"0","allowMargin":"1","isMinorCurrency":"0","minorToNormalRatio":"1.0","overdraft":"0.00000000","marginExposure":"0","exchangeRateUSD":"1.08580886E-5","currencylogourl":"\\/images\\/currencies\\/BTC.PNG","AVGCost_DefaultCurrency":"0","DefaultCurrencyRatio":"1.00","UnRealized_DefaultCurrency":"0","SoldValue_DefaultCurrency":"0","RealizedPL_DefaultCurrency":"0"}],"Positions":[{"symbol":"BTCUSDT","PortfolioWeight":"0","marketSymbol":"ZENQ","currencySymbol":"USDT-Binance","quantity":"1.02788","lastPrice":"91996.99000000","lastDelta":"792.99","deltaPercent":"0.86947","totalMarketValue":"94561.8660812","totalMarketValueInDefault":"0","averageCost":"71970.58895273","securityType":"Crypto Asset","CustodianID":"0","subUserId":"0","priceDecimal":"3","marketId":"118","contractSize":"1","tickerId":"32777","reserved":"0","available":"1.02788","custodianName":"MKT","bep":"71970.58895273","idcSymbol":"","feedMarketSymbol":"","feedSource":"","isin":"","symbolID":"BTCUSDT","BloombergSymbol":"","DescriptionEN":"Bitcoin","DescriptionAR":"Bitcoin","lastBid":"91996.99000000","lastAsk":"91997.00000000","lastVolume":"2303263217","MarginPaid":"73977.128972733","totalCost":"73977.128972733","UnrealizedPL":"20584.737108468","UnrealizedPLInDefault":"19485.7412982277739766228","UnrealizedPLPercent":"27.83","AvgCostRealizedPLAdjusted":"71970.58895273","initialMargin":"0","securityTypeId":"16","bondMaturityDate":"1900-01-01","bondFaceValue":"100.0","bondDistributionPercent":"0.0","bondYieldPercent":"0","bondDistributionsPerYear":"0","QuantityDecimal":"8","CurrencyDecimals":"2","PendingQuantity":"0","FuturesOptionsExpiryDate":"1900-01-01","UnderlyingTickerID":"0","UnderlyingSymbol":"","OptionType":"","OptionStrikePrice":"0.0","CryptoSymbolBought":"BTC","CryptoSymbolSold":"USDT","dayGainLocal":"771.58137182886","costLocal":"70027.573809857","marketValueLocal":"89513.31510905","realizedGainLocal":"1.0725104127225","accruedInterest":"0","bondRatingStandardAndPoors":"","accumulatedCoupon":"0","averageCostComm":"71970.58895273","actualCost":"73977.128972733","actualCostInDefault":"70027.5738063864951610293","plPercentage":"27.827343929575","bidYTM":"0.0","unrealizedGLComm":"20584.737108468","realizedPL":"1.133","PendingQuantityBuy":"0","PendingQuantitySell":"0","actualCostLocal":"70027.573809857","unrealizedPLLocal":"19485.741299193","symbolAlias":"BTCUSDT","symbolAlias2":"BTC","dayGain":"815.0985612","subUserNameEN":"Main","lastPrevPrice":"91203.99","priceCurrencySymbol":"USDT-Binance","unrealizedPL_NoPLAdded":"20584.737108468","unrealizedPLUSD":"20584.737108468","marketValueUSD":"94561.8660812","takeProfitAmount":"0","takeProfitStr":"","takeProfitQty":"0","stopLossAmount":"0","stopLossStr":"","stopLossQty":"0","hasTrigger":"0","BondNextDistributionDate":"1900-01-01","marginRequiredPercent":0}],"Equity":[{"EquityValue":"114786.07","MarginRatio":"%100.00","CurrencySymbol":"EUR","requiredDeposit":0,"requiredSelling":0,"CurrencyDecimals":"2"}],"Totals":[{"TotalCost":"0.00","TotalMarketValue":"0.00","TotalGainLoss":"19485.74","TotalMarginRequired":"70027.57","CurrencySymbol":"EUR","CurrencyDecimals":"2","NonCashMarginRationPercent":"0.00","DailyUnrealizedPnL":"771.59","DailyUnrealizedPnLPercent":"0.67","DailyRealizedPnL":"","DailyRealizedPnLPercent":"","DailyTotalPnL":"","DailyTotalPnLPercent":"","CurrencyDecimalsPreferred":"2"}],"TotalBySecurityType":[{"SecurityType":"Crypto Asset","TotalMarketValueLocalCurrency":"89513.31510905","CurrencyDecimalLocal":"2","TotalMarketValueUSD":"94561.8660812","UnrealizedPLLocal":"19485.741299193","UnrealizedPLUSD":"20584.737108468","CurrencyDecimalUSD":"2","SecurityTypeID":"16"}]},"errors":[],"extra":[]}'
        # b'{"code":"R200","data":{"customerId":"1000432","Balances":[{"currencySymbol":"EUR","precision":"2","cashBalance":"0","availableForTrading":"0","availableForWithdrawal":"0","reserved":"0","currencyDesc":"EUR","suspendedCurrency":"0","rate":0.94589481649639995}],"Positions":[],"Equity":[{"EquityValue":"0.00","MarginRatio":"%100.00","CurrencySymbol":"EUR","requiredDeposit":0,"requiredSelling":0,"CurrencyDecimals":"2"}],"Totals":[{"TotalCost":"0.00","TotalMarketValue":"0.00","TotalGainLoss":"0.00","TotalMarginRequired":"0.00","CurrencySymbol":"EUR","CurrencyDecimals":"2","NonCashMarginRationPercent":"0.00","DailyUnrealizedPnL":"","DailyUnrealizedPnLPercent":"","DailyRealizedPnL":"","DailyRealizedPnLPercent":"","DailyTotalPnL":"","DailyTotalPnLPercent":"","CurrencyDecimalsPreferred":"2"}],"TotalBySecurityType":[]},"errors":[],"extra":[]}'
        # b'{"code":"R403","data":[],"errors":"You are not authorized to view this information","extra":[]}'
        # b'{"code":"R400","data":[],"errors":"Customer Does not exist","extra":[]}'
        status_code = data.get('code', '')

        content = data.get('data', [])
        if content != []:
            customerId = content.get('customerId', '')
            Balances = content.get('Balances', '')
            Positions = content.get('Positions', '')
            Equity = content.get('Equity', '')
            Totals = content.get('Totals', '')
            TotalBySecurityType = content.get('TotalBySecurityType', '')
            error = data.get('errors', [])
            is_error = False
        else:
            message = data.get('errors', [])
            error = message[0]
            customerId = ""
            Balances = ""
            Positions = ""
            Equity = ""
            Totals = ""
            TotalBySecurityType = ""
            is_error = True

        return cls(
            status_code=status_code,
            customerId=customerId,
            Balances=Balances,
            Positions=Positions,
            Equity=Equity,
            Totals=Totals,
            TotalBySecurityType=TotalBySecurityType,
            error=error,
            is_error=is_error
        )