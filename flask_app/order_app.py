import json

from flask import jsonify, request

from flask_app import app, db
from flask_app.models import Order
from flask_app.constants import Transaction

from pprint import pprint


def data_processing(data: dict):
    Transaction.ID = data["ID"]
    Transaction.StartedOn = data["StartedOn"]
    Transaction.FinishedOn = data["FinishedOn"]
    Transaction.State = data["State"]
    Transaction.LocationName = data["LocationName"]
    Transaction.LocationNo = data["LocationNo"]
    Transaction.TransactionNo = data["TransactionNo"]
    Transaction.TerminalNo = data["TerminalNo"]
    Transaction.EmployeeNo = data["EmployeeNo"]
    Transaction.EmployeName = data["EmployeName"]
    Transaction.Net = data["Net"]
    Transaction.Tax = data["Tax"]
    Transaction.Gross = data["Gross"]
    Transaction.Payment = data["Payment"]
    Transaction.IsRefund = data["IsRefund"]
    Transaction.created_at = data["created_at"]
    pprint(Transaction.StartedOn)


@app.route('/api/order_stream', methods=['POST'])
def add_data():
    data = request.get_json()
    order_data = json.dumps(data)
    # print(order_data, type(order_data))
    dict_order_data = eval(order_data)
    data_processing(dict_order_data)
    # print(dict_order_data["Items"][0]['AddedOn']) # доступ к словарю по ключу
    new_order = Order(data=order_data)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Data added successfully'}), 201


# if __name__ == '__main__':
#     app.run(debug=True)
