import json
from tqdm import tqdm

from flask import jsonify, request, make_response
from flask_httpauth import HTTPBasicAuth

from flask_app import app, db
from flask_app.gbq import GBQ
from flask_app.models import Order
from flask_app.data_processing import (
    data_processing_products,
    data_processing_invoices,
    data_processing_discounts,
    data_processing_payments,
)
from flask_app.validators import validate_field_json
from flask_app.constants import (
    SECRET_PATH,
    SET_PROJECT,
    DATASET_NAME,
    JSON_ERROR,
    INVOICE,
    INVOICE_DISCOUNTS,
    INVOICE_PRODUCTS,
    TB_ERROR,
    MESSAGE,
    DATA_ADD_SUCCES,
    DF_ERROR,
    INVOICE_PAYMENTS,
    USERS,
    EMPTY_JSON,
    JSON_WITHOUT_FIELD,
)
from flask_app.send_message import send_message


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username in USERS and USERS[username] == password:
        return username


@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error": "Unauthorized access"}), 401)


def record_logs(order_data):
    """Записывает словарь полученныи из json в БД в качестве логов."""
    new_order = Order(data=order_data)
    db.session.add(new_order)
    db.session.commit()


def save_to_google(data, table_name):
    """Преобразует словарь в датасет и записывает в GBQ."""
    my_gbq = GBQ(secret_path=SECRET_PATH)
    my_gbq.set_project(SET_PROJECT)
    return my_gbq.insert_rows_to_table([data], DATASET_NAME, table_name)


@app.route("/api/order_stream", methods=["POST"])
@auth.login_required
def add_data():
    """Главная функция, получает request и управляет всей логикой."""
    data = request.get_json()
    if not data:
        send_message(EMPTY_JSON)
        return jsonify({MESSAGE: JSON_ERROR}), 400
    if "Items" not in data and "Discounts" not in data and "Payments" not in data:
        send_message(JSON_WITHOUT_FIELD)
        return jsonify({MESSAGE: JSON_ERROR}), 400
    order_data = json.dumps(data)
    record_logs(order_data)

    validation_errors = validate_field_json(data)
    if validation_errors:
        for error in tqdm(validation_errors):
            send_message(error)
            return jsonify({MESSAGE: JSON_ERROR}), 400
    else:
        invoices = data_processing_invoices(data)
        products = data_processing_products(data)
        discounts = data_processing_discounts(data)
        payments = data_processing_payments(data)

        if discounts:
            for d in tqdm(discounts):
                result = save_to_google(d.dict(), INVOICE_DISCOUNTS)
                if result is False:
                    send_message(TB_ERROR + INVOICE_DISCOUNTS)

        if invoices and products and payments:

            result = save_to_google(invoices.dict(), INVOICE)
            if result is False:
                send_message(TB_ERROR + INVOICE)

            for p in tqdm(products):
                result = save_to_google(p.dict(), INVOICE_PRODUCTS)
                if result is False:
                    send_message(TB_ERROR + INVOICE_PRODUCTS)

            for pay in tqdm(payments):
                result = save_to_google(pay.dict(), INVOICE_PAYMENTS)
                if result is False:
                    send_message(TB_ERROR + INVOICE_PAYMENTS)

            return jsonify({MESSAGE: DATA_ADD_SUCCES}), 200

        return jsonify({MESSAGE: DF_ERROR}), 400
