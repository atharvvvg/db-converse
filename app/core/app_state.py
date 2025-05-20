# app/core/app_state.py
class AppState:
    def __init__(self):
        self.db_connection = None
        self.db_name = None

# Global instance (simple approach for now)
current_app_state = AppState() 