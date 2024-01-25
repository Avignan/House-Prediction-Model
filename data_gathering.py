import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

env_path = r"your_env_path"

# Load variables from the .env file into the environment
load_dotenv(dotenv_path=env_path)


username = os.getenv("db_user")
password = os.getenv("db_password")
hostname = os.getenv("db_server")
port = os.getenv("db_port")
database = os.getenv("db_database")
table = os.getenv("db_table")

credential_dict = {
    'username': username,
    'password': password,
    'hostname': hostname,
    'port': port,
    'database': database,
    'table': table
}


def connect_2_mysql_db(creds: dict):
    try:
        # Establish a connection to the database
        mydb = mysql.connector.connect(
            host=creds['hostname'],
            user=creds['username'],
            password=creds['password'],
            database=creds['database']
        )

        cursor_obj = mydb.cursor()
        return mydb, cursor_obj
    except ConnectionError as connection_error:
        print(connection_error, flush=True)
        return None


def fetch_table_data_from_db(creds: dict):
    house_data = None
    connection_obj, connection_cursor = connect_2_mysql_db(creds)
    try:
        if connection_cursor:
            table_data_query = f"SELECT * FROM {creds['table']}"
            connection_cursor.execute(table_data_query)
            result = connection_cursor.fetchall()
            columns_list = [i[0] for i in connection_cursor.description]
            house_data = pd.DataFrame(result, columns=columns_list)
            connection_cursor.close()
            connection_obj.close()
        return house_data
    except Exception as data_fetching_error:
        print(data_fetching_error, flush=True)
        return house_data


if __name__ == "__main__":
    fetch_table_data_from_db(credential_dict)