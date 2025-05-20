import customtkinter as ctk
from ui.connect_dialog import ConnectDialog
from services import db_service
from core.app_state import current_app_state
from ui.converse_frame import ConverseFrame
from ui.dashboard_frame import DashboardFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DB-Converse")
        self.geometry("800x600")

        self.connection_status_label = ctk.CTkLabel(self, text="Status: Not Connected")
        self.connection_status_label.pack(pady=10)

        self.connect_button = ctk.CTkButton(self, text="Connect to Database", command=self.open_connect_dialog)
        self.connect_button.pack(pady=10)

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=(0,10))

        self.tab_view.add("Converse")
        self.tab_view.add("Dashboard")

        self.converse_frame = ConverseFrame(self.tab_view.tab("Converse"))
        self.converse_frame.pack(fill="both", expand=True)

        self.dashboard_frame = DashboardFrame(self.tab_view.tab("Dashboard"))
        self.dashboard_frame.pack(fill="both", expand=True)

        self.dashboard_frame.load_dashboard_data()

    def open_connect_dialog(self):
        dialog = ConnectDialog(self)
        details = dialog.get_details()
        if details:
            if current_app_state.db_connection:
                db_service.disconnect_from_db(current_app_state.db_connection)

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
                current_app_state.db_connection = None
                current_app_state.db_name = None
                self.connection_status_label.configure(text="Status: Connection Failed")
            
            self.dashboard_frame.load_dashboard_data()
        else:
            print("Connection dialog cancelled or closed.")
            self.dashboard_frame.load_dashboard_data()

if __name__ == "__main__":
    app = App()
    app.mainloop()
    if current_app_state.db_connection:
        db_service.disconnect_from_db(current_app_state.db_connection) 