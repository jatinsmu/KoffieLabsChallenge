import sqlite3
import pandas as pd


def create_connection(db):
    """
    Create connection to the sqlite database. If the database is not present yet, it will create one.
    :param db: name of the database, example 'cache.db' -> string
    :return: Connection object
    """
    try:
        # connection object for db
        connection = sqlite3.connect(db)
        return connection
    except sqlite3.Error as error:
        print("Error while creating connection to the database: ", error)
        return None


def create_table(connection):
    """
    Create a table named vin_details if it does not already exist
    :param connection: Database connection object
    :return: None
    """
    try:
        cursor = connection.cursor()
        # Create vin_details table if not exists
        create_query = '''CREATE TABLE IF NOT EXISTS vin_details 
                        ( Vin           TEXT,
                          Make          TEXT,
                          Model         TEXT,
                          Model_Year    TEXT,
                          Body_Class    TEXT
                         );'''
        cursor.execute(create_query)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to create table in sqlite db: ", error)
    finally:
        connection.close()


def insert_data(connection, data):
    """
    Insert data into the table named vin_details
    :param connection: Database Connection Object
    :param data: Data to be entered in Dictionary format
    :return: None
    """
    try:
        cursor = connection.cursor()
        vin = data['VIN']
        make = data['Make']
        model = data['Model']
        model_year = data['Model Year']
        body_class = data['Body Class']

        insert_query = "INSERT INTO vin_details VALUES ('{}','{}','{}','{}','{}');".format(vin, make, model, model_year, body_class)
        cursor.execute(insert_query)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert record in sqlite db: ", error)
    finally:
        connection.close()


def get_data(connection, vin):
    """
    Return details of Vin if present in database
    :param connection: Database Connection Object
    :param vin: Alphanumeric string of length 17
    :return: Vin details in List of tuples object
    """
    try:
        cursor = connection.cursor()
        select_query = "SELECT * from vin_details WHERE Vin='{}'".format(vin)
        cursor.execute(select_query)
        result = cursor.fetchall()

        if len(result)>0:
            return result # list of tuples
        else:
            return None

    except sqlite3.Error as error:
        print("Failed to get record from sqlite db: ", error)
    finally:
        connection.close()


def delete_data(connection, vin):
    """
    Delete data from table if record exists
    :param connection: Database Connection Object
    :param vin: Alphanumeric string of length 17
    :return: Boolean True or False
    """
    try:
        cursor = connection.cursor()
        delete_query = "DELETE from vin_details WHERE Vin='{}'".format(vin)
        cursor.execute(delete_query)
        connection.commit()
        return True

    except sqlite3.Error as error:
        print("Failed to insert record in sqlite db: ", error)
        return False
    finally:
        connection.close()


def export_db(connection):
    """
    Export the database as a parquet file and save on local disk
    :param connection: Database Connection Object
    :return: Boolean True or False
    """
    try:
        select_query = "SELECT * FROM vin_details"
        df = pd.read_sql_query(select_query, connection)
        df.to_parquet('export.parquet')
        print("Database export successful")
        return True
    except Exception as error:
        print("Failed to export db: ", error)
        return False
    finally:
        connection.close()