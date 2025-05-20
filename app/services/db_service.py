import mysql.connector
from mysql.connector import Error

def connect_to_db(host, user, password, database_name):
    """Establishes a connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database_name
        )
        if connection.is_connected():
            print(f"Successfully connected to database: {database_name}")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
    return connection # Should be None if not connected

def disconnect_from_db(connection):
    """Closes the database connection."""
    if connection and connection.is_connected():
        connection.close()
        print("MySQL connection is closed.") 