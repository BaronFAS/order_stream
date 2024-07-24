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
SECRET_PATH2 = "eco-condition-429319-v2-ed22b29980a1.json"
SET_PROJECT = "posbistro-x-klasna"
SET_PROJECT2 = "eco-condition-429319-v2"
DATASET_NAME = "Piotrkowska"
DATASET_NAME_REBERNIA = "Rebernia_Manufaktura"
MESSAGE = "message"
VALIDATE_ERROR = "No field "
JSON_ERROR = "Error at data json"
INVOICE = "invoices"
INVOICE_PRODUCTS = "invoice_products"
INVOICE_DISCOUNTS = "invoice_discounts"
INVOICE_PAYMENTS = "invoice_payments"
TB_ERROR = "Failed to save to table: "
DATA_ADD_SUCCES = "Data added successfully"
DF_ERROR = "Error at data field"
DATA_PROCESSING_ERROR = "Error while processing data:"
EMPTY_JSON = "I received empty json"
JSON_WITHOUT_FIELD = 'I received json without the field or fields "Items", "Discounts", "Payments"'
ID_ERROR = "The file has this ID"

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
        "Invoice": ["companyName", "street", "streetNumber", "postCode", "city", "taxNumber"]
    },
    "Barcode",
    "Client",
    "LoyaltyCard",
    "DeliveryAddress",
]
