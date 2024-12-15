# **ZenQ Exchange Python Client Documentation**

---
Official implementation of the ZenQ APIs for Python 3.8+

## **Table of Contents**
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Classes](#classes)
4. [Methods](#methods)
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
The installation can be performed by use the `pip install` command.
At first download file with .whl extension.

```bash
pip install downloaded_file.whl
```
Ensure that API variables are properly configured in the `config.py` file.

---
## **Usage**
Fast and basic example, check below for methods details.
```python
# import client for manage connection to Zenq
from zenqapi import Client 

# create an object client
client = Client(apiSecret="aaa", apiKey="bbb", test=True)

# import a specific ticker or * for all ticker available on exchange
from zenqapi import BTCUSDC

# base call to exchange
client.search_ticker(BTCUSDC)

from zenqapi import *
client.search_ticker(ETHUSDT)

```

## **Classes**

### **`Client`**
The main class to interact with the Zenq API.

#### **Constructor**
```python
from zenqapi import Client

client = Client(apiSecret="aaa", apiKey="bbb", test=True)
```

- **Parameters**
  - `apiKey` (str): API key generated from the exchange.
  - `apiSecret` (str): API secret key associated with the API key.
  - `test` (bool, optional): Flag to specify the environment (True = test environment, False = production).

---

## **Methods**

---

### **1. place_limit_order**

#### **Description**
Places a limit order on the exchange by specifying quantity, price, order type, and ticker.

#### **Signature**
```python
place_limit_order(apiQuantity: float, apiOrderType: Union[int, str], apiPrice: float, apiTickerId: Union[int, str]) -> APIStandardResponse
```

#### **Parameters**
- `apiQuantity` (float): Quantity of the order in base token units.
- `apiOrderType` (Union[int, str]): Type of the order (e.g., "buy", "sell", 1, or -1).
- `apiPrice` (float): Price limit for the order.
- `apiTickerId` (Union[int, str]): Ticker identifier (e.g., "BTCUSDT" or internal ticker ID).

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
client = Client(apiKey="your_key", apiSecret="your_secret", test=True)
response = client.place_limit_order(apiQuantity=1.0, apiOrderType="buy", apiPrice=50000, apiTickerId="BTCUSDT")
print(response.message)
```

---

### **2. place_market_order**

#### **Description**
Places a market order on the exchange.

#### **Signature**
```python
place_market_order(apiQuantity: float, apiOrderType: Union[int, str], apiTickerId: int) -> APIStandardResponse
```

#### **Parameters**
- `apiQuantity` (float): Quantity of the order.
- `apiOrderType` (Union[int, str]): Type of the order (e.g., "buy", "sell", 1, or -1).
- `apiTickerId` (int): Ticker identifier.

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
search_ticker(symbol: Union[int, str]) -> APIStandardResponse
```

#### **Parameters**
- `symbol` (Union[int, str]): Symbol or ticker ID (e.g., "BTCUSDT").

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
order_list(apiTickerId: Union[int, str] = "", orderId: str = "") -> APIStandardResponse
```

#### **Parameters**
- `apiTickerId` (Union[int, str], optional): Ticker ID to filter by.
- `orderId` (str, optional): Specific order ID to filter by.

#### **Return**
See `place_limit_order`.

#### **Example**
```python
response = client.order_list(apiTickerId="BTCUSDT")
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
- `apiTickerId` (Union[int, str], optional): Ticker ID.

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
order_cancel(orderId: str, apiTickerId: Union[int, str] = "") -> APIStandardResponse
```

#### **Parameters**
- `orderId` (str): Unique identifier of the order to cancel.
- `apiTickerId` (Union[int, str], optional): Ticker ID.

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

Copyright 2024 Zenq

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
