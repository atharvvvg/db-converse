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

def get_table_names(connection):
    """Fetches a list of table names from the connected database."""
    if not connection or not connection.is_connected():
        print("Not connected to a database.")
        return []
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [table[0] for table in cursor.fetchall()]
        return tables
    except Error as e:
        print(f"Error fetching table names: {e}")
        return []
    finally:
        if cursor:
            cursor.close()

def get_basic_schema_string(connection):
    """Returns a simple string representation of the schema (table names)."""
    table_names = get_table_names(connection)
    if not table_names:
        return "No tables found or unable to fetch schema."
    return f"Tables: {', '.join(table_names)}" 