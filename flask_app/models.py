from datetime import datetime as dt

from pydantic import BaseModel

from flask_app import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)


class TransactionModel(BaseModel):
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
    created_at: dt


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
    created_at: dt


# class Discount(db.Model):
#     __tablename__ = 'discounts'

#     id = db.Column(db.String, primary_key=True)
#     added_on = db.Column(db.DateTime)
#     item_id = db.Column(db.String)
#     name = db.Column(db.String)
#     amount = db.Column(db.Float)
#     transaction_id = db.Column(db.String, db.ForeignKey('transactions.id'), nullable=False)


# class Payment(db.Model):
#     __tablename__ = 'payments'

#     id = db.Column(db.String, primary_key=True)
#     added_on = db.Column(db.DateTime)
#     type = db.Column(db.String)
#     amount = db.Column(db.Float)
#     transaction_id = db.Column(db.String, db.ForeignKey('transactions.id'), nullable=False)
