import customtkinter as ctk
from ui.widgets.chart_widget import ChartWidget
from services import chart_service, db_service
from core.app_state import current_app_state
import seaborn as sns # For styling
# import matplotlib.pyplot as plt # Not strictly needed here unless modifying plt state directly

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.chart_widgets = [] # To keep track of chart widgets

        # Apply a modern, minimal theme once for charts
        # You can choose different styles: "whitegrid", "darkgrid", "white", "ticks"
        # Palettes: "muted", "pastel", "viridis", "rocket", etc.
        sns.set_theme(style="whitegrid", palette="muted")
        # plt.style.use('seaborn-v0_8-whitegrid') # Example for older matplotlib/seaborn

        self.label = ctk.CTkLabel(self, text="Dashboard Summary", font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(pady=10)

        self.refresh_button = ctk.CTkButton(self, text="Refresh Dashboard", command=self.load_dashboard_data)
        self.refresh_button.pack(pady=5)

        self.charts_container = ctk.CTkFrame(self) # A frame to hold charts
        self.charts_container.pack(fill="both", expand=True, padx=5, pady=5)

    def load_dashboard_data(self):
        # Clear existing charts
        for widget in self.charts_container.winfo_children():
            widget.destroy()
        self.chart_widgets.clear()

        if not current_app_state.db_connection:
            no_conn_label = ctk.CTkLabel(self.charts_container, text="Connect to a database to view dashboard.")
            no_conn_label.pack(pady=20)
            return

        # MVP: Chart of table row counts (example)
        try:
            table_names = db_service.get_table_names(current_app_state.db_connection)
            if not table_names:
                no_tables_label = ctk.CTkLabel(self.charts_container, text="No tables found in the database.")
                no_tables_label.pack(pady=20)
                return

            row_counts = []
            valid_table_names = []
            for table in table_names:
                # Important: Sanitize table name if it comes from user input. Here it's from SHOW TABLES.
                # For schema generated names, this is safer.
                df_count, err = db_service.execute_query(current_app_state.db_connection, f"SELECT COUNT(*) as count FROM `{table}`")
                if not err and not df_count.empty:
                    row_counts.append(df_count['count'].iloc[0])
                    valid_table_names.append(table)
                else:
                    print(f"Could not get row count for table {table}: {err}")

            if valid_table_names and row_counts:
                fig = chart_service.generate_bar_chart_figure(
                    labels=valid_table_names,
                    values=row_counts,
                    title="Row Counts per Table",
                    xlabel="Table Name",
                    ylabel="Number of Rows"
                )
                chart_frame = ctk.CTkFrame(self.charts_container) # Frame for each chart
                chart_frame.pack(pady=5, padx=5, fill="x") # Or use grid

                chart_w = ChartWidget(chart_frame, fig)
                chart_w.pack(fill="both", expand=True)
                self.chart_widgets.append(chart_w)
            else:
                no_data_label = ctk.CTkLabel(self.charts_container, text="No data to display for row counts.")
                no_data_label.pack(pady=20)

        except Exception as e:
            print(f"Error loading dashboard data: {e}")
            error_label = ctk.CTkLabel(self.charts_container, text=f"Error loading dashboard: {e}")
            error_label.pack(pady=20) 