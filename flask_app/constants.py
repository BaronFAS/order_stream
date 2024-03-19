import os
import json

from dotenv import load_dotenv

from flask_app import app

load_dotenv()

app.config["FLASK_APP"] = os.getenv("FLASK_APP")
app.config["FLASK_ENV"] = os.getenv("FLASK_ENV")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

USERS_JSON = os.getenv("USERS_JSON")
USERS = json.loads(USERS_JSON)

SECRET_PATH = "posbistro-x-klasna-0596bf139c12.json"
SET_PROJECT = "posbistro-x-klasna"
DATASET_NAME = "Manufaktura"
MESSAGE = "message"
VALIDATE_ERROR = "Нет поля "
JSON_ERROR = "Error at data json"
INVOICE = "invoices"
INVOICE_PRODUCTS = "invoice_products"
INVOICE_DISCOUNTS = "invoice_discounts"
INVOICE_PAYMENTS = "invoice_payments"
TB_ERROR = "Failed to save to table: "
DATA_ADD_SUCCES = "Data added successfully"
DF_ERROR = "Error at data field"
DATA_PROCESSING_ERROR = "Ошибка при обработке данных: "
EMPTY_JSON = "Пришел пустой json"
JSON_WITHOUT_FIELD = 'Пришел json без поля или полей "Items", "Discounts", "Payments"'


REQUIRED_FIELDS_TRANSACTION = [
    "ID",
    "StartedOn",
    "FinishedOn",
    "State",
    "LocationName",
    "LocationNo",
    "TransactionNo",
    "TerminalNo",
    "EmployeeNo",
    "EmployeeName",
    "Net",
    "Tax",
    "Gross",
    "Payment",
    "IsRefund",
    {
        "Items": [
            "AddedOn",
            "ID",
            "SKU",
            "PLU",
            "EAN",
            "Name",
            "Category",
            "UnitPrice",
            "Quantity",
            "TaxRate",
            "Tax",
            "Amount",
        ],
        "Discounts": ["AddedOn", "ID", "ItemID", "Name", "Amount"],
        "Payments": ["AddedOn", "ID", "Type", "Amount"],
    },
    "Barcode",
    "Client",
    "LoyaltyCard",
    "DeliveryAddress",
    "Invoice",
]
