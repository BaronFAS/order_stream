from typing import TypedDict, NewType

Timestamp = NewType("Timestamp", int)


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
    "IsRefund"
]


class Transaction(TypedDict):
    ID: str
    StartedOn: str
    FinishedOn: str
    State: str
    LocationName: str
    LocationNo: str
    TransactionNo: str
    TerminalNo: str
    EmployeeNo: str
    EmployeName: str
    Net: float
    Tax: float
    Gross: float
    Payment: float
    IsRefund: bool
    created_at: Timestamp
