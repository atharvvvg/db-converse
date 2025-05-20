import customtkinter as ctk
from ui.connect_dialog import ConnectDialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DB-Converse")
        self.geometry("800x600")
        details = ConnectDialog(self).get_details()
        print(f"Connection details received: {details}")
        # Potentially set appearance mode early
        # ctk.set_appearance_mode("System") # Light, Dark, System
        # ctk.set_default_color_theme("blue") # blue, green, dark-blue

if __name__ == "__main__":
    app = App()
    app.mainloop() 