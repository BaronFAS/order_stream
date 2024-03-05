import json
from tqdm import tqdm

import pandas as pd
from flask import jsonify, request

from flask_app import app, db
from flask_app.gbq import GBQ
from flask_app.models import Order
from flask_app.data_processing import (
    data_processing_products,
    data_processing_transaction,
    data_processing_discounts,
    data_processing_payments,
)
from flask_app.validators import validate_field
from flask_app.constants import (
    SECRET_PATH,
    SET_PROJECT,
    DATASET_NAME,
    VALIDATE_ERROR,
    JSON_ERROR,
    INVOICE,
    INVOICE_DISCOUNTS,
    INVOICE_PRODUCTS,
    TB_ERROR,
    MESSAGE,
    DATA_ADD_SUCCES,
    DF_ERROR,
    INVOICE_PAYMENTS,
)
from flask_app.send_message import send_message


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
    return my_gbq.write_df_to_bgq(df, DATASET_NAME, table_name)


@app.route("/api/order_stream", methods=["POST"])
def add_data():
    """Главная функция, получает request и управляет всей логикой."""
    data = request.get_json()
    order_data = json.dumps(data)
    record_logs(order_data)
    dict_order_data = eval(order_data)
    validation_errors = validate_field(dict_order_data)
    if validation_errors:
        for error in tqdm(validation_errors):
            send_message(VALIDATE_ERROR + error)
            return jsonify({MESSAGE: JSON_ERROR}), 400
    else:
        transaction = data_processing_transaction(dict_order_data)
        products = data_processing_products(dict_order_data)
        discounts = data_processing_discounts(dict_order_data)
        payments = data_processing_payments(dict_order_data)

        if transaction and products and discounts and payments:

            result = save_to_google(transaction.dict(), INVOICE)
            if result is False:
                send_message(TB_ERROR + INVOICE)

            for p in tqdm(products):
                result = save_to_google(p.dict(), INVOICE_PRODUCTS)
                if result is False:
                    send_message(TB_ERROR + INVOICE_PRODUCTS)

            for d in tqdm(discounts):
                result = save_to_google(d.dict(), INVOICE_DISCOUNTS)
                if result is False:
                    send_message(TB_ERROR + INVOICE_DISCOUNTS)

            for pay in tqdm(payments):
                result = save_to_google(pay.dict(), INVOICE_PAYMENTS)
                if result is False:
                    send_message(TB_ERROR + INVOICE_PAYMENTS)

            return jsonify({MESSAGE: DATA_ADD_SUCCES}), 201

        return jsonify({MESSAGE: DF_ERROR}), 400
