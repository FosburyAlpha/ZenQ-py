from typing import Union


def filter_order_by_ticker_name(list_of_order: list, ticker_name: str):
    ticker_name_order_list = []
    for item in list_of_order:
        if item['Symbol'] == ticker_name:
            ticker_name_order_list.append(item)
    return ticker_name_order_list


def filter_order_by_ticker_name_and_order_id(list_of_order: list, order_id: str, ticker_name: str):
    order_list = []
    for item in list_of_order:
        if item['TickerID'] == ticker_name:
            if item['OrderID'] == order_id:
                order_list.append(item)
    return order_list


def filter_order_by_order_id(list_of_order: list, order_id: str):
    order_list = []
    for item in list_of_order:
        if item['OrderID'] == order_id:
            order_list.append(item)
    return order_list


def filter_order(list_of_order: dict, ticker_name: str, order_id: Union[str, int]):
    order_id = str(order_id)

    list_of_order_1 = list_of_order.get('data', [])

    if len(list_of_order_1) > 0:
        list_of_order_1 = list_of_order['data']

        if ticker_name == "" and order_id == "":
            return list_of_order

        elif ticker_name != "" and order_id != "":
            return filter_order_by_ticker_name_and_order_id(list_of_order=list_of_order_1, ticker_name=ticker_name,
                                                            order_id=order_id)
        elif ticker_name != "" and order_id == "":
            return filter_order_by_ticker_name(list_of_order=list_of_order_1, ticker_name=ticker_name)

        elif ticker_name == "" and order_id != "":
            return filter_order_by_order_id(list_of_order=list_of_order_1, order_id=order_id)
    else:
        return list_of_order
