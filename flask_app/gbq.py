import os
import warnings
from google.cloud import bigquery


class GBQ:
    def __init__(self, secret_path: str):
        warnings.filterwarnings("ignore")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = secret_path

    def set_project(self, project_id):
        self.project_id = project_id
        self.__client = bigquery.Client(project=project_id)

    def select_rows_from_table(self, id, dataset, table):
        print(id)
        table_id = dataset + "." + table
        query = f"SELECT ID FROM {table_id} WHERE ID='{id}'"
        query_job = self.__client.query(query)  # API request
        return query_job.result().total_rows  # Waits for statement to finish

    def update_rows_in_table(self, data, dataset, table, key='ID'):
        data = vars(data)
        data = {k: '' if v is None else v for k, v in data.items()}  # Заменяем значения None на пустые строки
        table_id = dataset + "." + table
        print(data, type(data))
        id = data['ID']
        set_data = ', '.join([f"{k} = '{v}'" if type(v) == str else f"{k} = {v}" for k,v in data.items()])
        dml_statement = f"UPDATE {table_id} SET {set_data} WHERE {key} = '{id}'"
        query_job = self.__client.query(dml_statement)  # API request
        return query_job.result()  # Waits for statement to finish

    def insert_rows_to_table(self, data, dataset, table):
        # print(data)
        table_id = dataset + "." + table
        errors = self.__client.insert_rows_json(table_id, data)
        if not len(errors):
            return True
        print(errors)
        return False

    def delete_rows_from_table(self, id_key, id_value, dataset, table):
        print(id)
        table_id = dataset + "." + table
        query = f"DELETE FROM {table_id} WHERE {id_key}='{id_value}'"
        query_job = self.__client.query(query)  # API request
        return query_job.result().total_rows  # Waits for statement to finish


if __name__ == '__main__':
    SECRET_PATH = "posbistro-x-klasna-0596bf139c12.json"
    SET_PROJECT = "posbistro-x-klasna"
    DATASET_NAME = "Piotrkowska"
    my_gbq = GBQ(secret_path=SECRET_PATH)
    my_gbq.set_project(SET_PROJECT)
    id = '8f0658a6-36f0-4dc0-83fa-839d1e625a56'
    table = 'invoices'
    res = my_gbq.select_rows_from_table(id, DATASET_NAME, table)
    print(res)
    # my_gbq.update_rows_in_table('test_postman')
    print(1)
