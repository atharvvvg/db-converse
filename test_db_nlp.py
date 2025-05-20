from app.services import db_service
import pandas as pd # Make sure pandas is imported for the test script too

    # ---- Assuming 'conn' is an active MySQL connection object ----
    # Example: (replace with your actual connection setup)
conn = db_service.connect_to_db("localhost", "root", "root", "db_converse")

if conn:
    print("Executing query: SELECT * FROM test_mvp;")
    df, err = db_service.execute_query(conn, "SELECT * FROM test_mvp;")

    if err:
        print(f"Error: {err}")
    elif df.empty:
        print("Query executed, but no results returned or table is empty.")
    else:
        print("Query successful. Results:")
        print(df)

        # Test a non-SELECT query (should be blocked by current MVP logic)
    print("\nExecuting non-SELECT query (expecting error): INSERT INTO test_mvp VALUES (3, 'Charlie');")
    df_insert, err_insert = db_service.execute_query(conn, "INSERT INTO test_mvp VALUES (3, 'Charlie');")
    if err_insert:
        print(f"Blocked as expected: {err_insert}")
    else:
        print("Non-SELECT query was not blocked (this is unexpected for MVP).")


        # Don't forget to disconnect if you established a new connection for this test
        db_service.disconnect_from_db(conn)
else:
    print("Cannot test execute_query without an active database connection.")