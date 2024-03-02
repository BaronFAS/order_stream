# REQUIRED_FIELDS_TRANSACTION = [
#     "ID",
#     "StartedOn",
#     "FinishedOn",
#     "State",
#     "LocationName",
#     "LocationNo",
#     "TransactionNo",
#     "TerminalNo",
#     "EmployeeNo",
#     "EmployeName",
#     "Net",
#     "Tax",
#     "Gross",
#     "Payment",
#     "IsRefund",
# ]

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
        "Items": ["AddedOn", "ID", "SKU", "PLU", "EAN", "Name", "Category", "UnitPrice", "Quantity", "TaxRate", "Tax", "Amount"],
        "Discounts": ["AddedOn", "ID", "ItemID", "Name", "Amount"],
        "Payments": ["AddedOn", "ID", "Type", "Amount"]
    }
]
