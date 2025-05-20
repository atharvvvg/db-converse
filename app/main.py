import customtkinter as ctk
from ui.connect_dialog import ConnectDialog
from services import db_service
from core.app_state import current_app_state
from ui.converse_frame import ConverseFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DB-Converse")
        self.geometry("800x600")

        self.connection_status_label = ctk.CTkLabel(self, text="Status: Not Connected")
        self.connection_status_label.pack(pady=10)

        self.connect_button = ctk.CTkButton(self, text="Connect to Database", command=self.open_connect_dialog)
        self.connect_button.pack(pady=10)

        self.converse_frame = ConverseFrame(self)
        self.converse_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def open_connect_dialog(self):
        dialog = ConnectDialog(self)
        details = dialog.get_details()
        if details:
            # Disconnect existing if any
            if current_app_state.db_connection:
                db_service.disconnect_from_db(current_app_state.db_connection)
                current_app_state.db_connection = None
                current_app_state.db_name = None

            conn = db_service.connect_to_db(
                details["host"],
                details["user"],
                details["password"],
                details["database"]
            )
            if conn:
                current_app_state.db_connection = conn
                current_app_state.db_name = details["database"]
                self.connection_status_label.configure(text=f"Status: Connected to {details['database']}")
            else:
                self.connection_status_label.configure(text="Status: Connection Failed")
                # Optionally show an error message dialog
        else:
            print("Connection dialog cancelled or closed.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
    # Ensure disconnection on app close
    if current_app_state.db_connection:
        db_service.disconnect_from_db(current_app_state.db_connection) 