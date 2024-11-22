# **ZenQ Exchange Python Client Documentation**

---
Official implementation of the ZenQ APIs for Python 3.8+

## **Table of Contents**
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Classes](#classes)
4. [Signatures](#signatures)
5. [Tickers](#Tickers)
6. [Methods](#methods)
   - [place_limit_order](#place_limit_order)
   - [place_market_order](#place_market_order)
   - [search_ticker](#search_ticker)
   - [order_list](#order_list)
   - [order_modify](#order_modify)
   - [order_cancel](#order_cancel)
   - [user_balances](#user_balances)

---

## **Introduction**
This library allows interaction with the **ZenQ Exchange**, enabling order management (limit/market), symbol lookups, order listings, modifications, cancellations, and user balance retrieval.

---

## **Installation**
The installation can be performed by use the `pip install` command along with the Git repository URL

```bash
pip install git+https://github.com/FosburyAlpha/ZenQ-py.git
```

---

## **Client initialization**

The main class to interact with the Zenq API.

Create a client instance to enable API management:

```python
client = Client(apiKey= "xxx", apiSecret= "yyy")
```

- **Parameters**
  - `apiKey` (str): API key generated from the exchange.
  - `apiSecret` (str): API secret key associated with the API key.
  - `test` (optional bool): Flag to specify the environment True = test environment, False = production. By default, value is False.

---
## **Signatures**

There are two main signatures returned by methods:
- `APIStandardResponse`
- `APIUserBalances`

### **1. APIStandardResponse**
All methods have this type of object as response.

- **Attributes**
  - `status_code` (str): The raw status code of server response.
  - `order_id` (str): The order_id code from server response if valorized otherwise is 0.
  - `message` (str): The message of server response, it contains the content, also errors.
  - `is_error` (bool): A flag that is True if the call returned a not 2XX code.

```python
obj_response_from_api.message
```


### **2. APIUserBalances**
Only user_balances method have this type of object as response.

- **Attributes**
  - `status_code` (str): The raw status code of server response.
  - `customerId` (str): The unique identifier for the customer associated with the response.
  - `Balances` (str): A detailed representation of the user's account balances.
  - `Positions` (str): Information about the user's open positions in various instruments or assets.
  - `Equity` (str): The user's total equity, representing the value of all assets minus liabilities.
  - `Totals` (str): Aggregated financial data, summarizing key metrics such as balances and equity.
  - `error` (str): Error details or messages, if any, returned by the API.
  - `is_error` (bool): A flag that is True if the call returned a not 2XX code.
```python
obj_response_from_api.Equity
```

---
## **Tickers**
All methods that have `ApiTickerID` can accept a usefull object that library can offer.
For use it you have to import the tickers class like:

```python
from api.tickers import *
```

And then you have the all ZenQ's tickers property ready to use.
```python
BTCUSDT -> Object
BTCUSDT.ticker_id -> The serialized apiTickerID (BTCUSDT=32777)
BTCUSDT.ticker_name -> The serialized apiTickerID (BTCUSDT="BTCUSDT")
```

---
## **Methods**


### **1. place_limit_order**

#### **Description**
Places a limit order on the exchange by specifying quantity, price, order type, and ticker.

#### **Signature**
```python
place_limit_order(apiQuantity: float, apiOrderType: Union[int, str], apiPrice: float, apiTickerId: Union[int, str, Ticker]) -> APIStandardResponse
```

#### **Parameters**
- `apiQuantity` (float): Quantity of the order in base token units.
- `apiOrderType` (Union[int, str]): Type of the order (e.g., "buy", "sell", 1, or -1).
- `apiPrice` (float): Price limit for the order.
- `apiTickerId` (Union[int, str, Ticker]): This can be a string, the ticker ID from the Zenq exchange, or the ticker Object from library.
                       E.g. ADAUSDC, "ADAUSDC", 40895, ADAUSDC.ticker_id

#### **Exceptions**
- `ValueError`: Raised if `apiOrderType` or `apiTickerId` is invalid.

#### **Return**
- `APIStandardResponse`: Object containing:
  - `status_code`: The response status code.
  - `order_id`: The ID of the created order (if available).
  - `message`: The response message.
  - `is_error`: True if the call failed.

#### **Example**
```python
response = client.place_limit_order(apiQuantity=1.0, apiOrderType="buy", apiPrice=50000, apiTickerId=BTCUSDT)
print(response.message)
```

---

### **2. place_market_order**

#### **Description**
Places a market order on the exchange.

#### **Signature**
```python
place_market_order(apiQuantity: float, apiOrderType: Union[int, str], apiTickerId: Union[int, str, Ticker]) -> APIStandardResponse
```

#### **Parameters**
- `apiQuantity` (float): Quantity of the order.
- `apiOrderType` (Union[int, str]): Type of the order (e.g., "buy", "sell", 1, or -1).
- `apiTickerId` (Union[int, str, Ticker]): This can be a string, the ticker ID from the Zenq exchange, or the ticker Object from library.
                       E.g. ADAUSDC, "ADAUSDC", 40895, ADAUSDC.ticker_id

#### **Return**
See `place_limit_order`.

#### **Example**
```python
response = client.place_market_order(apiQuantity=0.5, apiOrderType="sell", apiTickerId=123)
print(response.status_code)
```

---

### **3. search_ticker**

#### **Description**
Retrieves information about a specific symbol.

#### **Signature**
```python
search_ticker(symbol: Union[int, str, Ticker]) -> APIStandardResponse
```

#### **Parameters**
- `symbol` (Union[int, str, Ticker]): This can be a string, the ticker ID from the Zenq exchange, or the ticker Object from library.
                       E.g. ADAUSDC, "ADAUSDC", 40895, ADAUSDC.ticker_id

#### **Return**
See `place_limit_order`.

#### **Example**
```python
response = client.search_ticker(symbol="BTCUSDT")
print(response.message)
```

---

### **4. order_list**

#### **Description**
Fetches a filtered list of orders, optionally filtered by ticker ID or order ID.

#### **Signature**
```python
order_list(apiTickerId: Union[int, str, Ticker] = "", orderId: str = "") -> APIStandardResponse
```

#### **Parameters**
- `apiTickerId` (Union[int, str, Ticker], optional): Ticker ID to filter by. This can be a string, the ticker ID from the Zenq exchange, or the ticker Object from library.
                       E.g. ADAUSDC, "ADAUSDC", 40895, ADAUSDC.ticker_id
- `orderId` (str, optional): Specific order ID to filter by.

#### **Return**
See `place_limit_order`.

#### **Example**
```python
response = client.order_list()
print(response.message)
```

---

### **5. order_modify**

#### **Description**
Modifies an existing order by updating its price and quantity.

#### **Signature**
```python
order_modify(orderId: str, newPrice: float, newQuantity: float, marketValue: float, apiTickerId: Union[int, str] = 0) -> APIStandardResponse
```

#### **Parameters**
- `orderId` (str): Unique identifier of the order to modify.
- `newPrice` (float): New price for the order.
- `newQuantity` (float): New quantity for the order.
- `marketValue` (float): Current market value for validation.
- `apiTickerId` (Union[int, str], optional): This can be a string, the ticker ID from the Zenq exchange, or the ticker Object from library.
                       E.g. ADAUSDC, "ADAUSDC", 40895, ADAUSDC.ticker_id

#### **Return**
See `place_limit_order`.

#### **Example**
```python
response = client.order_modify(orderId="12345", newPrice=55000, newQuantity=1.5, marketValue=54000)
print(response.message)
```

---

### **6. order_cancel**

#### **Description**
Cancels an existing order.

#### **Signature**
```python
order_cancel(orderId: str, apiTickerId: Union[int, str, Ticker] = "") -> APIStandardResponse
```

#### **Parameters**
- `orderId` (str): Unique identifier of the order to cancel.
- `apiTickerId` (Union[int, str, Ticker], optional): This can be a string, the ticker ID from the Zenq exchange, or the ticker Object from library.
                       E.g. ADAUSDC, "ADAUSDC", 40895, ADAUSDC.ticker_id

#### **Return**
See `place_limit_order`.

#### **Example**
```python
response = client.order_cancel(orderId="12345")
print(response.message)
```

---

### **7. user_balances**

#### **Description**
Fetches the balances of a user account.

#### **Signature**
```python
user_balances(userId: str = "") -> APIUserBalances
```

#### **Parameters**
- `userId` (str, optional): User ID. If empty, retrieves balances for the current API key.

#### **Return**
- `APIUserBalances`: Object containing user balance data.

#### **Example**
```python
response = client.user_balances()
print(response.data)
```

---

### **License**

Copyright 2024 ZenQ

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

