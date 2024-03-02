from datetime import datetime

from flask_app.models import TransactionModel, ProductsModel, DiscountsModel


def data_processing_transaction(dict_order_data):
    """Преобразует поля словаря в нужные типы данных,
    создает объект pydantic."""
    try:
        data_transaction = {
            "ID": dict_order_data["ID"],
            "StartedOn": dict_order_data["StartedOn"],
            "FinishedOn": dict_order_data["FinishedOn"],
            "State": dict_order_data["State"],
            "LocationName": dict_order_data["LocationName"],
            "LocationNo": dict_order_data["LocationNo"],
            "TransactionNo": dict_order_data["TransactionNo"],
            "TerminalNo": dict_order_data["TerminalNo"],
            "EmployeeNo": dict_order_data["EmployeeNo"],
            "EmployeName": dict_order_data["EmployeName"],
            "Net": dict_order_data["Net"],
            "Tax": dict_order_data["Tax"],
            "Gross": dict_order_data["Gross"],
            "Payment": dict_order_data["Payment"],
            "IsRefund": dict_order_data["IsRefund"],
            "created_at": datetime.now(),
        }
        transaction = TransactionModel(**data_transaction)
        return transaction
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")


def data_processing_products(dict_order_data):
    """Преобразует поля словаря в нужные типы данных,
    создает объект pydantic."""
    try:
        products = []
        data_products = dict_order_data["Items"]
        for data in data_products:
            data = {
                "invoice_id": dict_order_data["ID"],
                "AddedOn": data["AddedOn"],
                "ID": data["ID"],
                "SKU": data["SKU"],
                "PLU": data["PLU"],
                "EAN": data["EAN"],
                "Name": data["Name"],
                "Category": data["Category"],
                "UnitPrice": data["UnitPrice"],
                "Quantity": data["Quantity"],
                "TaxRate": data["TaxRate"],
                "Tax": data["Tax"],
                "Amount": data["Amount"],
                "created_at": datetime.now(),
            }
            products.append(ProductsModel(**data))

        return products
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")


def data_processing_discounts(dict_order_data):
    """Преобразует поля словаря в нужные типы данных,
    создает объект pydantic."""
    try:
        discounts = []
        data_discounts = dict_order_data["Discounts"]
        for data in data_discounts:
            data = {
                "invoice_id": dict_order_data["ID"],
                "AddedOn": data["AddedOn"],
                "ID": data["ID"],
                "ItemID": data["ItemID"],
                "Name": data["Name"],
                "Amount": data["Amount"],
                "created_at": datetime.now(),
            }
            discounts.append(DiscountsModel(**data))

        return discounts
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")
