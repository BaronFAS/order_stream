import os
import json
from datetime import datetime
from tqdm import tqdm

from flask import jsonify, request, make_response
from flask_httpauth import HTTPBasicAuth

from flask_app import app
from flask_app.gbq import GBQ
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
    INVOICE_PAYMENTS,
    USERS,
    EMPTY_JSON,
    JSON_WITHOUT_FIELD,
    DF_ERROR,
    ID_ERROR,
    DATASET_NAME_REBERNIA,
    SECRET_PATH2,
    SET_PROJECT2,
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
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log_entry = timestamp + '|' + order_data
    logs_folder = 'data'
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    file_path = os.path.join(logs_folder, 'app.log')

    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        if file_size > 10 * 1024 * 1024:
            new_file_path = os.path.join(logs_folder, 'app_old.log')
            os.rename(file_path, new_file_path)
            file_path = os.path.join(logs_folder, 'app.log')

    with open(file_path, 'a') as file:
        file.write(json.dumps(log_entry) + '\n')


def save_to_google(data, table_name):
    """Преобразует словарь в датасет и записывает в GBQ."""
    my_gbq = GBQ(secret_path=SECRET_PATH)
    my_gbq.set_project(SET_PROJECT)
    return my_gbq.insert_rows_to_table([data], DATASET_NAME, table_name)


def check_and_write_id(id_to_check):
    file_name = 'invoices_id.log'
    logs_folder = 'data'
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    file_path = os.path.join(logs_folder, file_name)
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if id_to_check in line and "test_postman" not in line:
                    return False
        with open(file_path, 'a') as file:
            file.write(id_to_check + '\n')
        return True
    except FileNotFoundError:
        with open(file_path, 'w') as file:
            file.write(id_to_check + '\n')
        return True


@app.route("/api/order_stream", methods=["POST"])
@auth.login_required
def add_data():
    """Главная функция, получает request и управляет всей логикой."""
    data = request.get_json()
    if not data:
        send_message(EMPTY_JSON)
        return jsonify({MESSAGE: JSON_ERROR}), 400
    if "Items" not in data and "Discounts" not in data and "Payments" not in data: # noqa
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

        if invoices:
            print(invoices)
            invoices_id = check_and_write_id(invoices.ID)
            if not invoices_id:
                return jsonify({MESSAGE: ID_ERROR}), 200
            result = save_to_google(invoices.dict(), INVOICE)
            print(f"Это инвойс {result}")
            if result is False:
                send_message(TB_ERROR + INVOICE)
                return jsonify({MESSAGE: DF_ERROR}), 400
        if discounts:
            for d in tqdm(discounts):
                result = save_to_google(d.dict(), INVOICE_DISCOUNTS)
                print(f"Это дискаунт {result}")
                if result is False:
                    send_message(TB_ERROR + INVOICE_DISCOUNTS)
                    return jsonify({MESSAGE: DF_ERROR}), 400
        if products:
            for product in tqdm(products):
                result = save_to_google(product.dict(), INVOICE_PRODUCTS)
                print(f"Это продукт {result}")
                if result is False:
                    send_message(TB_ERROR + INVOICE_PRODUCTS)
                    return jsonify({MESSAGE: DF_ERROR}), 400
        if payments:
            for pay in tqdm(payments):
                result = save_to_google(pay.dict(), INVOICE_PAYMENTS)
                print(f"Это паиментс {result}")
                if result is False:
                    send_message(TB_ERROR + INVOICE_PAYMENTS)
                    return jsonify({MESSAGE: DF_ERROR}), 400

        return jsonify({MESSAGE: DATA_ADD_SUCCES}), 200


def save_to_google2(data, table_name):
    """Преобразует словарь в датасет и записывает в GBQ."""
    my_gbq = GBQ(secret_path=SECRET_PATH2)
    my_gbq.set_project(SET_PROJECT2)
    return my_gbq.insert_rows_to_table(
        [data], DATASET_NAME_REBERNIA, table_name
    )


@app.route("/api/rebernia", methods=["POST"])
@auth.login_required
def add_data2():
    """Главная функция, получает request и управляет всей логикой."""
    data = request.get_json()
    if not data:
        send_message(EMPTY_JSON)
        return jsonify({MESSAGE: JSON_ERROR}), 400
    if "Items" not in data and "Discounts" not in data and "Payments" not in data: # noqa
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

        if invoices:
            print(invoices)
            invoices_id = check_and_write_id(invoices.ID)
            if not invoices_id:
                return jsonify({MESSAGE: ID_ERROR}), 200
            result = save_to_google2(invoices.dict(), INVOICE)
            print(f"Это инвойс {result}")
            if result is False:
                send_message(TB_ERROR + INVOICE)
                return jsonify({MESSAGE: DF_ERROR}), 400
        if discounts:
            for d in tqdm(discounts):
                result = save_to_google2(d.dict(), INVOICE_DISCOUNTS)
                print(f"Это дискаунт {result}")
                if result is False:
                    send_message(TB_ERROR + INVOICE_DISCOUNTS)
                    return jsonify({MESSAGE: DF_ERROR}), 400
        if products:
            for product in tqdm(products):
                result = save_to_google2(product.dict(), INVOICE_PRODUCTS)
                print(f"Это продукт {result}")
                if result is False:
                    send_message(TB_ERROR + INVOICE_PRODUCTS)
                    return jsonify({MESSAGE: DF_ERROR}), 400
        if payments:
            for pay in tqdm(payments):
                result = save_to_google2(pay.dict(), INVOICE_PAYMENTS)
                print(f"Это паиментс {result}")
                if result is False:
                    send_message(TB_ERROR + INVOICE_PAYMENTS)
                    return jsonify({MESSAGE: DF_ERROR}), 400

        return jsonify({MESSAGE: DATA_ADD_SUCCES}), 200
