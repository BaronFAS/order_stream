from pydantic import BaseModel, Field
from typing import Optional


class InvoicesModel(BaseModel):
    ID: str
    StartedOn: str
    FinishedOn: str
    State: str
    LocationName: str
    LocationNo: str
    TransactionNo: str
    TerminalNo: str
    EmployeeNo: int
    EmployeeName: str
    Net: float
    Tax: float
    Gross: float
    Payment: float
    IsRefund: bool
    Barcode: str
    Client: Optional[str] = Field(..., nullable=True)
    LoyaltyCard: Optional[str] = Field(..., nullable=True)
    DeliveryAddress: Optional[str] = Field(..., nullable=True)
    Invoice: Optional[str] = Field(..., nullable=True)
    additional: Optional[str] = Field(..., nullable=True)
    created_at: str


class ProductsModel(BaseModel):
    invoice_id: str
    AddedOn: str
    ID: str
    SKU: str
    PLU: str
    EAN: str
    Name: str
    Category: str
    UnitPrice: float
    Quantity: int
    TaxRate: float
    Tax: float
    Amount: float
    additional: Optional[str] = Field(..., nullable=True)
    created_at: str


class DiscountsModel(BaseModel):
    invoice_id: str
    AddedOn: str
    ID: str
    ItemID: str
    Name: str
    Amount: float
    additional: Optional[str] = Field(..., nullable=True)
    created_at: str


class PaymentsModel(BaseModel):
    invoice_id: str
    AddedOn: str
    ID: str
    Type: str
    Amount: float
    additional: Optional[str] = Field(..., nullable=True)
    created_at: str
