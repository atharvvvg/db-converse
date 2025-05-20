import customtkinter as ctk

class ConnectDialog(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Connect to MySQL")
        self.geometry("350x280")
        self.lift() # Bring to front
        self.attributes("-topmost", True) # Keep on top
        self.grab_set() # Modal behavior

        self.connection_details = None # To store result

        self.label_host = ctk.CTkLabel(self, text="Host:")
        self.label_host.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_host = ctk.CTkEntry(self, placeholder_text="localhost")
        self.entry_host.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.label_user = ctk.CTkLabel(self, text="User:")
        self.label_user.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_user = ctk.CTkEntry(self, placeholder_text="root")
        self.entry_user.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.label_password = ctk.CTkLabel(self, text="Password:")
        self.label_password.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_password = ctk.CTkEntry(self, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.label_db = ctk.CTkLabel(self, text="Database:")
        self.label_db.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_db = ctk.CTkEntry(self, placeholder_text="test_db")
        self.entry_db.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.connect_button = ctk.CTkButton(self, text="Connect", command=self._on_connect)
        self.connect_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

        self.grid_columnconfigure(1, weight=1)

    def _on_connect(self):
        self.connection_details = {
            "host": self.entry_host.get(),
            "user": self.entry_user.get(),
            "password": self.entry_password.get(),
            "database": self.entry_db.get()
        }
        self.destroy() # Close dialog

    def get_details(self):
        self.master.wait_window(self) # Wait for dialog to close
        return self.connection_details 