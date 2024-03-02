SECRET_PATH = "posbistro-x-klasna-0596bf139c12.json"
SET_PROJECT = "posbistro-x-klasna"
DATASET_NAME = "Manufaktura"
MESSAGE = "message"
VALIDATE_ERROR = "Нет поля "
JSON_ERROR = "Error at data json"
TB_INVOICE = "invoice"
TB_INVOICE_ERROR = f"It was not possible to save data to the {TB_INVOICE} table"  # noqa
INVOICE_PRODUCTS = "invoice_products"
INVOICE_PRODUCTS_ERROR = (
    f"It was not possible to save data to the {INVOICE_PRODUCTS} table"  # noqa
)
DATA_ADD_SUCCES = "Data added successfully"
DF_ERROR = "Error at data field"


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
