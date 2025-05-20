from app.services import db_service

# ---- IMPORTANT: Replace these with your actual test database details ----
test_host = ""  # Or your MySQL host IP/name
test_user = ""  # Your MySQL username
test_password = ""  # Your MySQL password
test_db_name = ""  # The name of your test database
# ---------------------------------------------------------------------

print(f"Attempting to connect to {test_db_name} on {test_host} with user {test_user}...")
conn = db_service.connect_to_db(test_host, test_user, test_password, test_db_name)

if conn:
    print("Connection test successful. Now attempting to disconnect.")
    db_service.disconnect_from_db(conn)
else:
    print("Connection test failed.")

print("Test script finished.")
