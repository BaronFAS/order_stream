import json

# from pprint import pprint

import pandas as pd
from flask import jsonify, request

from flask_app import app, db
from flask_app.gbq import GBQ
from flask_app.models import Order
from flask_app.data_processing import (
    data_processing_products,
    data_processing_transaction,
)
from flask_app.validators import validate_field
from flask_app.constants import (
    SECRET_PATH,
    SET_PROJECT,
    DATASET_NAME,
    VALIDATE_ERROR,
    JSON_ERROR,
    TB_INVOICE,
    TB_INVOICE_ERROR,
    INVOICE_PRODUCTS,
    INVOICE_PRODUCTS_ERROR,
    MESSAGE,
    DATA_ADD_SUCCES,
    DF_ERROR,
)


def record_logs(order_data):
    """Записывает словарь полученныи из json в БД в качестве логов."""
    new_order = Order(data=order_data)
    db.session.add(new_order)
    db.session.commit()


def save_to_google(data, table_name):
    """Преобразует словарь в датасет и записывает в GBQ."""
    my_gbq = GBQ(secret_path=SECRET_PATH)
    my_gbq.set_project(SET_PROJECT)
    df = pd.DataFrame([data], columns=data.keys())
    dataset_name = DATASET_NAME
    result = my_gbq.write_df_to_bgq(df, dataset_name, table_name)
    return result


@app.route("/api/order_stream", methods=["POST"])
def add_data():
    """Главная функция, получает request и управляет всей логикой."""
    data = request.get_json()
    order_data = json.dumps(data)
    record_logs(order_data)
    dict_order_data = eval(order_data)
    validation_errors = validate_field(dict_order_data)
    if validation_errors:
        for error in validation_errors:
            print(VALIDATE_ERROR + error)
            return jsonify({MESSAGE: JSON_ERROR}), 400
    else:
        transaction = data_processing_transaction(dict_order_data)
        products = data_processing_products(dict_order_data)

        if transaction and products:

            result = save_to_google(transaction.dict(), TB_INVOICE)
            if result is False:
                print(TB_INVOICE_ERROR)

            for p in products:
                result = save_to_google(p.dict(), INVOICE_PRODUCTS)
                if result is False:
                    print(INVOICE_PRODUCTS_ERROR)
            return jsonify({MESSAGE: DATA_ADD_SUCCES}), 201
        return jsonify({MESSAGE: DF_ERROR}), 400
