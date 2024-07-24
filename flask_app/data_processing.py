import json

from datetime import datetime

from flask_app.models import (
    InvoicesModel,
    ProductsModel,
    DiscountsModel,
    PaymentsModel,
)
from flask_app.constants import (
    DATA_PROCESSING_ERROR,
    INVOICE,
    INVOICE_PRODUCTS,
    INVOICE_DISCOUNTS,
    INVOICE_PAYMENTS,
)
from flask_app.send_message import send_message


def data_processing_invoices(dict_order_data):
    """Преобразует поля словаря в нужные типы данных,
    создает объект pydantic."""
    try:
        data_invoices = {
            "ID": dict_order_data["ID"],
            "StartedOn": dict_order_data["StartedOn"],
            "FinishedOn": dict_order_data["FinishedOn"],
            "State": dict_order_data["State"],
            "LocationName": dict_order_data["LocationName"],
            "LocationNo": dict_order_data["LocationNo"],
            "TransactionNo": dict_order_data["TransactionNo"],
            "TerminalNo": dict_order_data["TerminalNo"],
            "EmployeeNo": dict_order_data["EmployeeNo"],
            "EmployeeName": dict_order_data["EmployeeName"],
            "Net": dict_order_data["Net"],
            "Tax": dict_order_data["Tax"],
            "Gross": dict_order_data["Gross"],
            "Payment": dict_order_data["Payment"],
            "IsRefund": dict_order_data["IsRefund"],
            "Barcode": dict_order_data["Barcode"],
            "Client": dict_order_data["Client"],
            "LoyaltyCard": dict_order_data["LoyaltyCard"],
            "DeliveryAddress": dict_order_data["DeliveryAddress"],
            "Invoice": json.dumps(dict_order_data["Invoice"]),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        }
        additional_data = json.dumps(
            {
                key: value
                for key, value in dict_order_data.items()
                if key not in ["Items", "Discounts", "Payments"]
                and key not in data_invoices
            }
        )
        data_invoices["additional"] = additional_data
        invoices = InvoicesModel(**data_invoices)
        return invoices
    except Exception as e:
        send_message(DATA_PROCESSING_ERROR + str(e) + " в " + INVOICE)


def data_processing_products(dict_order_data):
    try:
        products = []
        data_products = dict_order_data["Items"]
        for data in data_products:
            new_data = {
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
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            }
            additional_data = {
                key: value
                for key, value in data.items()
                if key not in ['AddedOn', 'ID', 'SKU', 'PLU', 'EAN', 'Name', 'Category', 'UnitPrice', 'Quantity', 'TaxRate', 'Tax', 'Amount']
            }

            new_data["additional"] = str(additional_data)
            products.append(ProductsModel(**new_data))

        return products
    except Exception as e:
        send_message(DATA_PROCESSING_ERROR + str(e) + " в " + INVOICE_PRODUCTS)


def data_processing_discounts(dict_order_data):
    """Преобразует поля словаря в нужные типы данных,
    создает объект pydantic."""
    try:
        discounts = []
        data_discounts = dict_order_data["Discounts"]
        if data_discounts:
            for data in data_discounts:
                new_data = {
                    "invoice_id": dict_order_data["ID"],
                    "AddedOn": data["AddedOn"],
                    "ID": data["ID"],
                    "ItemID": data["ItemID"],
                    "Name": data["Name"],
                    "Amount": data["Amount"],
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                }
                additional_data = {
                    key: value
                    for key, value in data.items()
                    if key not in ['AddedOn', 'ID', "ItemID", 'Name', 'Amount']
                }
                new_data["additional"] = str(additional_data)
                discounts.append(DiscountsModel(**new_data))
        return discounts
    except Exception as e:
        send_message(DATA_PROCESSING_ERROR + str(e) + " в " + INVOICE_DISCOUNTS)


def data_processing_payments(dict_order_data):
    """Преобразует поля словаря в нужные типы данных,
    создает объект pydantic."""
    try:
        payments = []
        data_payments = dict_order_data["Payments"]
        for data in data_payments:
            new_data = {
                "invoice_id": dict_order_data["ID"],
                "AddedOn": data["AddedOn"],
                "ID": data["ID"],
                "Type": data["Type"],
                "Amount": data["Amount"],
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            }
            additional_data = {
                key: value
                for key, value in data.items()
                if key not in ['AddedOn', 'ID', "Type", 'Amount']
            }
            new_data["additional"] = str(additional_data)
            payments.append(PaymentsModel(**new_data))

        return payments
    except Exception as e:
        send_message(DATA_PROCESSING_ERROR + str(e) + " в " + INVOICE_PAYMENTS)
