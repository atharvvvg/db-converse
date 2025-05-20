import mysql.connector
from mysql.connector import Error
import pandas as pd

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

def execute_query(connection, query):
    """Executes a given SQL query and returns results as a Pandas DataFrame."""
    if not connection or not connection.is_connected():
        return pd.DataFrame(), "Error: Not connected to a database."
    
    # Basic safety for MVP: Allow SELECT and SHOW queries
    query_upper = query.strip().upper()
    if not query or not (query_upper.startswith("SELECT") or query_upper.startswith("SHOW")):
        return pd.DataFrame(), "Error: Only SELECT or SHOW queries are allowed for MVP."

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True) # Get results as dictionaries
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [i[0] for i in cursor.description] # Get column names
        df = pd.DataFrame(results, columns=column_names)
        return df, None # DataFrame, no error
    except Error as e:
        print(f"Error executing query '{query}': {e}")
        return pd.DataFrame(), f"Error executing query: {e}"
    finally:
        if cursor:
            cursor.close() 