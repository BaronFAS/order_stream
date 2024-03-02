SECRET_PATH = "posbistro-x-klasna-0596bf139c12.json"
SET_PROJECT = "posbistro-x-klasna"
DATASET_NAME = "Manufaktura"
MESSAGE = "message"
VALIDATE_ERROR = "Нет поля "
JSON_ERROR = "Error at data json"
INVOICE = "invoice"
INVOICE_PRODUCTS = "invoice_products"
INVOICE_DISCOUNTS = "invoice_discounts"
INVOICE_PAYMENTS = "invoice_payments"
TB_ERROR = "Failed to save to table: "
DATA_ADD_SUCCES = "Data added successfully"
DF_ERROR = "Error at data field"
DATA_PROCESSING_ERROR = "Ошибка при обработке данных: "

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
    "EmployeName",
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
]
