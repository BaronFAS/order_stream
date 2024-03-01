from flask_app import db
from datetime import datetime as dt
from pydantic import BaseModel


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


# class Transaction(db.Model):
#     __tablename__ = 'transactions'

#     id = db.Column(db.String, primary_key=True)
#     started_on = db.Column(db.DateTime)
#     finished_on = db.Column(db.DateTime)
#     state = db.Column(db.String)
#     location_name = db.Column(db.String)
#     location_no = db.Column(db.String)
#     transaction_no = db.Column(db.String)
#     terminal_no = db.Column(db.String)
#     employee_no = db.Column(db.String)
#     employee_name = db.Column(db.String)
#     net = db.Column(db.Float)
#     tax = db.Column(db.Float)
#     gross = db.Column(db.Float)
#     payment = db.Column(db.Float)
#     is_refund = db.Column(db.Boolean)
#     items = db.relationship('Item', backref='transaction', lazy=True)
#     discounts = db.relationship('Discount', backref='transaction', lazy=True)
#     payments = db.relationship('Payment', backref='transaction', lazy=True)


# class Item(db.Model):
#     __tablename__ = 'items'

#     id = db.Column(db.String, primary_key=True)
#     added_on = db.Column(db.DateTime)
#     sku = db.Column(db.String)
#     plu = db.Column(db.String)
#     ean = db.Column(db.String)
#     name = db.Column(db.String)
#     category = db.Column(db.String)
#     unit_price = db.Column(db.Float)
#     quantity = db.Column(db.Integer)
#     tax_rate = db.Column(db.Float)
#     tax = db.Column(db.Float)
#     amount = db.Column(db.Float)
#     transaction_id = db.Column(db.String, db.ForeignKey('transactions.id'), nullable=False)


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
