import sqlite3
from error import *


def create_connection(db_file: str) -> sqlite3.Connection:
    """
    Creates a connection to an SQLite database.

    This function attempts to create a connection to the SQLite database
    specified by the db_file parameter. If the connection is successful,
    it returns the connection object. If there is an error during the connection
    attempt, the error is printed, and None is returned.
    Args:
        db_file (str): The path to the SQLite database file.

    Returns:
        sqlite3.Connection or None: The connection object to the SQLite database,
        or None if the connection could not be established.
    """
    sql_connection = None

    try:
        sql_connection = sqlite3.connect(db_file)
        return sql_connection

    except sqlite3.Error as error_msg:
        error(error_msg)
        return sql_connection
    
def create_table(sql_connection: sqlite3.Connection, create_table_sql: str):
    """
    Creates a table in the SQLite database.

    This function executes the provided SQL statement to create a table
    in the SQLite database connected via sql_connection. It commits the 
    transaction if successful, and returns True. If an error occurs, it 
    triggers an error popup and returns False.

    Args:
        sql_connection (sqlite3.Connection): The connection object to the SQLite database.
        create_table_sql (str): The SQL statement to create the table.

    Returns:
        bool: True if the table is created successfully, False otherwise.
    """
    try:
        cursor = sql_connection.cursor()
        cursor.execute(create_table_sql)
        sql_connection.commit()
        cursor.close()
        return True
    except sqlite3.Error as error_msg:
        error(error_msg)
        return False
    
def insert_into_table(
    sql_connection: sqlite3.Connection, 
    insert_sql: str,
    data: list
):
    
    try:
        cursor = sql_connection.cursor()
        for item in data:
            cursor.execute(insert_sql, (item,))
        sql_connection.commit()
        cursor.close()
        return True
    
    except sqlite3.Error as error_msg:
        error(error_msg)
        return False
    
def get_all_data(
    sql_connection: sqlite3.Connection, 
    search_sql: str,

):
    try:
        cursor = sql_connection.cursor()
        cursor.execute(search_sql)
        result = cursor.fetchall()
        cursor.close()
        if result:
            return result
        else:
            return False
        
    except sqlite3.Error as error_msg:
        error(error_msg)
        return False

def get_column(connection: sqlite3.Connection, table_name:str, column_name:str) -> list:

    try:
        cursor = connection.cursor()
        query = f"SELECT {column_name} FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        column_data = [row[0] for row in rows]
        cursor.close()
 
        return column_data
    except sqlite3.Error as error_msg:
        error(error_msg)
        return []
    
def get_sql_column_names(connection: sqlite3.Connection, table_name: str):
   
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    column_names = [col[1] for col in columns_info]
    connection.close()
    
    return column_names

def remove_table(connection: sqlite3.Connection, table_name:str):

    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    connection.commit()
    connection.close()
    


