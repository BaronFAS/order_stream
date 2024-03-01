import os
import warnings
import pandas_gbq
from time import strftime
from google.cloud import bigquery


class GBQ:
    def __init__(self, secret_path: str):
        warnings.filterwarnings("ignore")
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = secret_path

    def set_project(self, project_id):
        self.project_id = project_id
        self.__client = bigquery.Client(project=project_id)

    def send_query(self, query):
        return pandas_gbq.read_gbq(query, self.project_id)

    def write_df_to_bgq(self, df, dataset, table, if_exists='append'):
        table_id = dataset + '.' + table
        pandas_gbq.to_gbq(df,
                          table_id,
                          project_id=self.project_id,
                          if_exists=if_exists,
                          progress_bar=False
                          )
        return True

    def get_table_columns(self, dataset, table):
        table_id = dataset + '.' + table
        columns = []
        table = self.__client.get_table(table_id)

        for field in table.schema:
            columns.append(field.name)
        return columns

    def set_new_schema(self, dataset, table, new_schema):
        gbq_schema = []
        for f in new_schema:
            gbq_schema.append(
                bigquery.SchemaField(f['name'], f['type'], description=f['description'])
            )

        table_id = dataset + '.' + table
        table = self.__client.get_table(table_id)

        table.schema = gbq_schema
        self.__client.update_table(table, ["schema"])
        return True

    def create_example_table(self, table_id):
        schema = [
            bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]

        table = bigquery.Table(table_id, schema=schema)
        table = self.__client.create_table(table)  # Make an API request.
        print(
            "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
        )

    def dataset_info(self, dataset_id):
        dataset = self.__client.get_dataset(dataset_id)  # Make an API request.

        full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
        friendly_name = dataset.friendly_name
        print(
            "Got dataset '{}' with friendly_name '{}'.".format(
                full_dataset_id, friendly_name
            )
        )

        # View dataset properties.
        print("Description: {}".format(dataset.description))
        print("Location: {}".format(dataset.location))

    def get_table_schema(self, dataset, table):
        table_id = dataset + '.' + table
        table = self.__client.get_table(table_id)
        schema = table.schema

        return schema

    def create_partition_table(self, dataset, table, schema, partition_field='date'):
        dataset_ref = bigquery.DatasetReference(self.project_id, dataset)
        table_ref = dataset_ref.table(table)

        table = bigquery.Table(table_ref, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field=partition_field,  # name of column to use for partitioning
        )

        table = self.__client.create_table(table)

        print(
            "Created table {}, partitioned on column {}".format(
                table.table_id, table.time_partitioning.field
            )
        )

    def write_df_to_bgq_with_partition(self, df, dataset, table, partition_field='date'):
        schema = self.get_table_schema(dataset, table)
        if len(schema) == 0:
            dtype_map = {'int64': 'INTEGER', 'int32': 'INTEGER', 'float64': 'FLOAT', 'object': 'STRING', 'datetime64[ns]': 'DATE'}
            dtype_lst = [dtype_map[d.name] for d in df.dtypes.to_list()]
            schema = list(map(lambda x, y: bigquery.SchemaField(x, y), df.columns.to_list(), dtype_lst))
            self.create_partition_table(dataset, table, schema, partition_field)

        job_config = bigquery.LoadJobConfig(
            # to append use "WRITE_APPEND" or don't pass job_config at all (appending is default)
            write_disposition="WRITE_TRUNCATE",
        )

        parts_lst = df[partition_field].value_counts().index.to_list()
        for partition in parts_lst:
            print(dataset, partition)
            # Include target partition in the table id:
            table_id = f"{self.project_id}.{dataset}.{table}${partition.strftime('%Y%m%d')}"
            job = self.__client.load_table_from_dataframe(
                df.loc[df[partition_field] == partition],
                table_id,
                job_config=job_config
            )  # Make an API request
            job.result()  # Wait for job to finish
            dt = strftime("[%Y-%b-%d %H:%M:%S]")
            message = f'{dt} Info: GBQ import to {dataset}.{table} with partition {partition}. ' \
                      f'Is error: {job.error_result}'
            print(message)
        return True


if __name__ == '__main__':
    import logging
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler(filename='../app.log', maxBytes=10000000, backupCount=10)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    query = """
        SELECT name, SUM(number) as total_people
        FROM `bigquery-public-data.usa_names.usa_1910_2013`
        WHERE state = 'TX'
        GROUP BY name, state
        ORDER BY total_people DESC
        LIMIT 20
    """
    my_gbq = GBQ()
    my_gbq.set_project(GBQ_PROJECT_ID)
    result = my_gbq.send_query(query)
    print(result)
    print(1)