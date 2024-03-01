import json

from flask import jsonify, request

from flask_app import app, db
from flask_app.models import Order
from flask_app.constants import Transaction, REQUIRED_FIELDS_TRANSACTION

from pprint import pprint
from datetime import datetime as dt


def validate_field(data):
    errors = []
    for field in REQUIRED_FIELDS_TRANSACTION:
        if field not in data:
            errors.append(f"Отсутствует обязательное поле '{field}'.")
    return errors


def data_processing(data):
    transaction = Transaction(
        ID=data["ID"],
        StartedOn=data["StartedOn"],
        FinishedOn=data["FinishedOn"],
        State=data["State"],
        LocationName=data["LocationName"],
        LocationNo=data["LocationNo"],
        TransactionNo=data["TransactionNo"],
        TerminalNo=data["TerminalNo"],
        EmployeeNo=data["EmployeeNo"],
        EmployeName=data["EmployeName"],
        Net=float(data["Net"]),
        Tax=float(data["Tax"]),
        Gross=float(data["Gross"]),
        Payment=float(data["Payment"]),
        IsRefund=bool(data["IsRefund"]),
        created_at=dt.now()
    )
    return transaction


def record_logs(order_data):
    new_order = Order(data=order_data)
    db.session.add(new_order)
    db.session.commit()


@app.route('/api/order_stream', methods=['POST'])
def add_data():
    data = request.get_json()
    order_data = json.dumps(data)
    dict_order_data = eval(order_data)
    validation_errors = validate_field(dict_order_data)
    if validation_errors:
        for error in validation_errors:
            print(error)
            record_logs(order_data)
            return jsonify({'message': 'Error data not added'}), 400
    else:
        transaction = data_processing(dict_order_data)
        record_logs(order_data)
        return jsonify({'message': 'Data added successfully'}), 201
