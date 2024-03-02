import json
# from pprint import pprint
from datetime import datetime

import pandas as pd
from flask import jsonify, request

from flask_app import app, db
from flask_app.constants import REQUIRED_FIELDS_TRANSACTION
from flask_app.gbq import GBQ
from flask_app.models import Order, TransactionModel


def validate_field(data):
    errors = []
    for field in REQUIRED_FIELDS_TRANSACTION:
        if field not in data:
            errors.append(f"Отсутствует обязательное поле '{field}'.")
    return errors


def data_processing(dict_order_data):
    try:
        data = {
            "ID": dict_order_data["ID"],
            "StartedOn": dict_order_data["StartedOn"],
            "FinishedOn": dict_order_data["FinishedOn"],
            "State": dict_order_data["State"],
            "LocationName": dict_order_data["LocationName"],
            "LocationNo": dict_order_data["LocationNo"],
            "TransactionNo": dict_order_data["TransactionNo"],
            "TerminalNo": dict_order_data["TerminalNo"],
            "EmployeeNo": dict_order_data["EmployeeNo"],
            "EmployeName": dict_order_data["EmployeName"],
            "Net": dict_order_data["Net"],
            "Tax": dict_order_data["Tax"],
            "Gross": dict_order_data["Gross"],
            "Payment": dict_order_data["Payment"],
            "IsRefund": dict_order_data["IsRefund"],
            # "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f %Z"),
            "created_at": datetime.now(),
        }
        transaction = TransactionModel(**data)
        # print(transaction)
        return transaction
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")


def record_logs(order_data):
    new_order = Order(data=order_data)
    db.session.add(new_order)
    db.session.commit()


def save_to_google(transaction):
    my_gbq = GBQ(secret_path="posbistro-x-klasna-0596bf139c12.json")
    my_gbq.set_project("posbistro-x-klasna")
    # print(pd.DataFrame([transaction]))
    df = pd.DataFrame([transaction], columns=transaction.keys())
    print(df.info())
    # print(df.info())
    dataset_name = "Manufaktura"
    table_name = "invoices"
    result = my_gbq.write_df_to_bgq(df, dataset_name, table_name)
    print(result)


@app.route("/api/order_stream", methods=["POST"])
def add_data():
    data = request.get_json()
    order_data = json.dumps(data)
    record_logs(order_data)
    dict_order_data = eval(order_data)
    validation_errors = validate_field(dict_order_data)
    if validation_errors:
        for error in validation_errors:
            print(f"Нет поля {error}")
            return jsonify({"message": "Error at data json"}), 400
    else:
        transaction = data_processing(dict_order_data)
        if transaction:
            print(type(transaction.dict()))
            save_to_google(transaction.dict())
            return jsonify({"message": "Data added successfully"}), 201
        return jsonify({"message": "Error at data field"}), 400
