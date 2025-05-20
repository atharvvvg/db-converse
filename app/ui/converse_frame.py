import customtkinter as ctk
from services import nlp_service, db_service
from core.app_state import current_app_state

class ConverseFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.nl_input_label = ctk.CTkLabel(self, text="Ask your database:")
        self.nl_input_label.pack(pady=(10,0), padx=10, anchor="w")

        self.nl_input_entry = ctk.CTkEntry(self, placeholder_text="e.g., show all customers")
        self.nl_input_entry.pack(fill="x", padx=10, pady=5)
        self.nl_input_entry.bind("<Return>", self._on_submit_query)


        self.submit_button = ctk.CTkButton(self, text="Submit Query", command=self._on_submit_query)
        self.submit_button.pack(pady=5, padx=10)

        self.sql_output_label = ctk.CTkLabel(self, text="Generated SQL:")
        self.sql_output_label.pack(pady=(10,0), padx=10, anchor="w")
        self.sql_output_text = ctk.CTkTextbox(self, height=60, wrap="word")
        self.sql_output_text.pack(fill="x", padx=10, pady=5)
        self.sql_output_text.configure(state="disabled")

        self.results_output_label = ctk.CTkLabel(self, text="Results:")
        self.results_output_label.pack(pady=(10,0), padx=10, anchor="w")
        self.results_output_text = ctk.CTkTextbox(self, height=150, wrap="none") # Use wrap="none" for tabular data
        self.results_output_text.pack(fill="both", expand=True, padx=10, pady=(5,10))
        self.results_output_text.configure(state="disabled")

    def _on_submit_query(self, event=None):
        nl_query = self.nl_input_entry.get()
        if not nl_query:
            self._update_results_text("Please enter a query.")
            return

        if not current_app_state.db_connection:
            self._update_results_text("Error: Not connected to a database.")
            return

        self._update_sql_text("Generating SQL...")
        self._update_results_text("Fetching results...")

        schema_str = db_service.get_basic_schema_string(current_app_state.db_connection)
        generated_sql_raw = nlp_service.nl_to_sql_basic(nl_query, schema_str)

        # Clean the generated SQL to remove markdown
        generated_sql = generated_sql_raw.strip()
        if generated_sql.startswith("```sql"):
            generated_sql = generated_sql[len("```sql"):].strip()
            if generated_sql.endswith("```"):
                generated_sql = generated_sql[:-len("```")].strip()
        elif generated_sql.startswith("```"): # Handle case where "sql" is missing
            generated_sql = generated_sql[len("```"):].strip()
            if generated_sql.endswith("```"):
                generated_sql = generated_sql[:-len("```")].strip()
        
        # Further cleanup: remove any remaining backticks if the SQL is simple and on one line
        # and was enclosed in single backticks by the LLM.
        if generated_sql.startswith("`") and generated_sql.endswith("`"):
            generated_sql = generated_sql[1:-1]


        self._update_sql_text(generated_sql if generated_sql else "Failed to generate SQL.")

        if generated_sql and not generated_sql.startswith("Error:"):
            df_results, error_msg = db_service.execute_query(current_app_state.db_connection, generated_sql)
            if error_msg:
                self._update_results_text(f"Error executing SQL: {error_msg}")
            elif df_results.empty:
                self._update_results_text("Query executed, no results returned or table is empty.")
            else:
                self._update_results_text(df_results.to_string())
        else:
            self._update_results_text("Cannot execute query due to SQL generation failure.")

    def _update_sql_text(self, text):
        self.sql_output_text.configure(state="normal")
        self.sql_output_text.delete("1.0", "end")
        self.sql_output_text.insert("1.0", text)
        self.sql_output_text.configure(state="disabled")

    def _update_results_text(self, text):
        self.results_output_text.configure(state="normal")
        self.results_output_text.delete("1.0", "end")
        self.results_output_text.insert("1.0", text)
        self.results_output_text.configure(state="disabled") 