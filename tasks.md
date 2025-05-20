Project Root: (Current Directory - all paths below are relative to this)

Pre-requisites for the LLM:

- Assume Python 3.9+ is installed.
- Assume `pip` is available.
- The LLM should create files and folders as specified, relative to the current working directory which is the project root.
- The LLM should be instructed to write runnable Python code and basic CustomTkinter UI elements.
- The LLM should know how to use `python-dotenv` for environment variables.

---

**Phase 1: Core Setup & Basic Window**

**Task 1.1: Initial Project Setup in Current Directory**

- **Start:** Current working directory is the designated project root.
- **Action:**
  1.  Inside the current directory (project root), create a Python virtual environment (e.g., `python -m venv .venv`).
  2.  Create `requirements.txt` in the project root with initial dependencies:
      ```
      customtkinter
      python-dotenv
      ```
  3.  Create `.gitignore` in the project root with common Python and venv entries (e.g., `/.venv`, `__pycache__/`, `*.pyc`, `.env`).
- **End:** Project root contains `.venv/`, `requirements.txt`, `.gitignore`.
- **Test:** Manually activate the virtual environment and run `pip install -r requirements.txt`.

**Task 1.2: Basic Application Entry Point and Empty Window**

- **Start:** `requirements.txt` installed from Task 1.1.
- **Action:**

  1.  Create `app/` directory in the project root.
  2.  Create `app/__init__.py` (can be empty).
  3.  Create `app/main.py` with:

      ```python
      import customtkinter as ctk

      class App(ctk.CTk):
          def __init__(self):
              super().__init__()
              self.title("DB-Converse")
              self.geometry("800x600")
              # Potentially set appearance mode early
              # ctk.set_appearance_mode("System") # Light, Dark, System
              # ctk.set_default_color_theme("blue") # blue, green, dark-blue

      if __name__ == "__main__":
          app = App()
          app.mainloop()
      ```

      Use code with caution.

- **End:** `app/main.py` created in the project root.
- **Test:** Run `python app/main.py` from the project root. An empty CustomTkinter window titled "DB-Converse" should appear.

**Task 1.3: Configuration for API Key (Google Gemini)**

- **Start:** `app/main.py` exists.
- **Action:**

  1.  Create `.env.example` in the project root with: `GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"`
  2.  Create `app/core/` directory in the project root.
  3.  Create `app/core/__init__.py` (empty).
  4.  Create `app/core/config.py` with:

      ```python
      import os
      from dotenv import load_dotenv

      load_dotenv() # Loads variables from .env file into environment

      GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

      # Basic check
      if not GOOGLE_API_KEY:
          print("WARNING: GOOGLE_API_KEY not found in .env file or environment variables.")
      ```

      Use code with caution.

- **End:** `.env.example` and `app/core/config.py` created in the project root.
- **Test:** Create a `.env` file in the project root (copy from `.env.example` and add a dummy key), then run `python -c "from app.core import config; print(config.GOOGLE_API_KEY)"` from the project root. It should print the dummy key or the warning if `.env` is misconfigured.

---

**Phase 2: Database Connection Service & Basic UI Integration**

**Task 2.1: Install MySQL Connector and Pandas**

- **Start:** `requirements.txt` exists.
- **Action:** Add `mysql-connector-python` and `pandas` to `requirements.txt`.
- **End:** `requirements.txt` updated.
- **Test:** Run `pip install -r requirements.txt` again from the project root.

**Task 2.2: Basic Database Service (`db_service.py`) - Connection Function**

- **Start:** `mysql-connector-python` installed.
- **Action:**

  1.  Create `app/services/` directory in the project root.
  2.  Create `app/services/__init__.py` (empty).
  3.  Create `app/services/db_service.py` with:

      ```python
      import mysql.connector
      from mysql.connector import Error

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
      ```

      Use code with caution.

- **End:** `app/services/db_service.py` with `connect_to_db` and `disconnect_from_db` created.
- **Test:** Manually create a small test script in the project root or use Python interactive mode:
  ```python
  from app.services import db_service
  # Replace with your actual test DB credentials
  conn = db_service.connect_to_db("localhost", "your_user", "your_password", "your_test_db")
  if conn:
      db_service.disconnect_from_db(conn)
  ```
  Use code with caution.
  (Ensure you have a test MySQL server running).

**Task 2.3: Simple Connection Dialog UI (`connect_dialog.py`)**

- **Start:** `app/services/db_service.py` has `connect_to_db`.
- **Action:**

  1.  Create `app/ui/` directory in the project root.
  2.  Create `app/ui/__init__.py` (empty).
  3.  Create `app/ui/connect_dialog.py` with:

      ```python
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
      ```

      Use code with caution.

- **End:** `app/ui/connect_dialog.py` created.
- **Test:** Modify `app/main.py` temporarily to open this dialog:
  ```python
  # In App class in main.py
  # ... (inside __init__)
  # from app.ui.connect_dialog import ConnectDialog # Add import
  # details = ConnectDialog(self).get_details()
  # print(f"Connection details received: {details}")
  ```
  Use code with caution.
  Run `python app/main.py` from the project root. The dialog should appear, and after filling and clicking "Connect", details should be printed.

**Task 2.4: Integrate Connection Dialog with `db_service` in Main App**

- **Start:** `app/ui/connect_dialog.py` and `app/services/db_service.connect_to_db` exist.
- **Action:**

  1.  Create `app/core/app_state.py` to hold the connection:

      ```python
      # app/core/app_state.py
      class AppState:
          def __init__(self):
              self.db_connection = None
              self.db_name = None

      # Global instance (simple approach for now)
      current_app_state = AppState()
      ```

      Use code with caution.

  2.  Modify `app/main.py`:

      ```python
      import customtkinter as ctk
      from app.ui.connect_dialog import ConnectDialog
      from app.services import db_service
      from app.core.app_state import current_app_state # Import app_state

      class App(ctk.CTk):
          def __init__(self):
              super().__init__()
              self.title("DB-Converse")
              self.geometry("800x600")

              self.connection_status_label = ctk.CTkLabel(self, text="Status: Not Connected")
              self.connection_status_label.pack(pady=10)

              self.connect_button = ctk.CTkButton(self, text="Connect to Database", command=self.open_connect_dialog)
              self.connect_button.pack(pady=10)

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
                      details["host"], details["user"], details["password"], details["database"]
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
      ```

      Use code with caution.

- **End:** `app/main.py` uses `ConnectDialog` and `db_service` to establish and display connection status. `app/core/app_state.py` created.
- **Test:** Run `python app/main.py` from the project root. Click "Connect to Database", enter valid credentials for your test DB. The status label should update to "Connected to [your_db_name]". Try with invalid credentials; status should be "Connection Failed".

---

**Phase 3: Basic NLP Service (Gemini) & Query Execution**

**Task 3.1: Install Google Gemini SDK**

- **Start:** `requirements.txt` exists.
- **Action:** Add `google-generativeai` to `requirements.txt`.
- **End:** `requirements.txt` updated.
- **Test:** Run `pip install -r requirements.txt` from the project root.

**Task 3.2: Basic NLP Service (`nlp_service.py`) - Simple Gemini Call**

- **Start:** `google-generativeai` installed, `app/core/config.py` has `GOOGLE_API_KEY`.
- **Action:** Create `app/services/nlp_service.py` with:
  ```python
  import google.generativeai as genai
  from app.core.config import GOOGLE_API_KEY

      if GOOGLE_API_KEY:
          genai.configure(api_key=GOOGLE_API_KEY)
          model = genai.GenerativeModel('gemini-pro') # Or 'gemini-1.5-flash' for faster, cheaper
      else:
          model = None
          print("NLP Service: Gemini API key not configured. NLP functionalities will be disabled.")

      def generate_text_with_gemini(prompt_text):
          """Generates text using Gemini based on a prompt."""
          if not model:
              return "Error: Gemini model not initialized (API key missing or invalid)."
          try:
              response = model.generate_content(prompt_text)
              # Basic error handling for response structure (may need refinement based on Gemini SDK)
              if response and response.candidates and response.candidates[0].content.parts:
                  return response.text
              else:
                  print(f"Gemini response issue: {response}")
                  return "Error: Received an unexpected response structure from Gemini."
          except Exception as e:
              print(f"Error during Gemini API call: {e}")
              return f"Error generating text: {e}"

      def nl_to_sql_basic(natural_language_query, db_schema_str=""):
          """
          Basic NL to SQL conversion.
          For MVP, db_schema_str might be simple like table names.
          """
          if not model:
              return "Error: Gemini model not initialized."

          prompt = f"""You are an expert SQL generator. Given the database schema (if provided) and a natural language question, generate a valid MySQL SQL query.

  Only output the SQL query. Do not include any explanations or markdown formatting.

Database Schema:
{db_schema_str if db_schema_str else "No schema provided. Assume common table names if necessary."}

Natural Language Question:
{natural_language_query}

SQL Query:
"""
return generate_text_with_gemini(prompt)
```
Use code with caution.

- **End:** `app/services/nlp_service.py` with basic Gemini interaction.
- **Test:**
  ```python
  # In Python interactive or a test script (in project root),
  # after activating venv and ensuring .env is set up
  from app.services import nlp_service
  # result = nlp_service.generate_text_with_gemini("Tell me a fun fact about Python programming.")
  # print(result)
  sql_query = nlp_service.nl_to_sql_basic("show me all users", "Tables: users (id, name, email)")
  print(f"Generated SQL: {sql_query}")
  ```

**Task 3.3: `db_service.py` - Get Basic Schema (Table Names)**

- **Start:** `app/services/db_service.py` exists.
- **Action:** Add to `app/services/db_service.py`:

  ```python
  # ... (imports and existing functions) ...

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
  ```

  Use code with caution.

- **End:** `app/services/db_service.py` can fetch table names.
- **Test:** With an active connection `conn` to your test DB (from Task 2.2 test):
  ```python
  # from app.services import db_service
  # schema_str = db_service.get_basic_schema_string(conn)
  # print(schema_str)
  ```
  Use code with caution.

**Task 3.4: `db_service.py` - Execute Generic Query and Fetch Results**

- **Start:** `app/services/db_service.py` exists.
- **Action:** Add to `app/services/db_service.py`:

  ```python
  # ... (imports and existing functions) ...
  import pandas as pd # Add pandas import

  def execute_query(connection, query):
      """Executes a given SQL query and returns results as a Pandas DataFrame."""
      if not connection or not connection.is_connected():
          return pd.DataFrame(), "Error: Not connected to a database."
      if not query or not query.strip().upper().startswith("SELECT"): # Basic safety for MVP
          return pd.DataFrame(), "Error: Only SELECT queries are allowed for MVP."

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
  ```

  Use code with caution.

- **End:** `app/services/db_service.py` can execute SELECT queries.
- **Test:** With an active connection `conn`:
  ```python
  # from app.services import db_service
  # Create a test table in your DB first, e.g., CREATE TABLE test_mvp (id INT, name VARCHAR(50));
  # INSERT INTO test_mvp VALUES (1, 'Alice'), (2, 'Bob');
  # df, err = db_service.execute_query(conn, "SELECT * FROM test_mvp;")
  # if err: print(err)
  # else: print(df)
  ```
  Use code with caution.

**Task 3.5: Basic "Converse" UI Frame and Integration**

- **Start:** `app/services/nlp_service.nl_to_sql_basic` and `app/services/db_service.execute_query` exist.
- **Action:**

  1.  Create `app/ui/converse_frame.py`:

      ```python
      import customtkinter as ctk
      from app.services import nlp_service, db_service
      from app.core.app_state import current_app_state

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
              generated_sql = nlp_service.nl_to_sql_basic(nl_query, schema_str)

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
      ```

      Use code with caution.

  2.  Integrate `ConverseFrame` into `app/main.py`:

      ```python
      # Add to imports in app/main.py:
      from app.ui.converse_frame import ConverseFrame

      # In App class __init__ after connect_button:
      # ...
      self.converse_frame = ConverseFrame(self)
      self.converse_frame.pack(fill="both", expand=True, padx=10, pady=10)
      ```

      Use code with caution.

- **End:** `app/ui/converse_frame.py` created and displayed in `main_window`.
- **Test:** Run `python app/main.py` from the project root. Connect to your DB. Type a simple NL query (e.g., "list all entries from test_mvp"). See if SQL is generated and results are displayed. Try a query that might fail.

---

**Phase 4: Basic Dashboard - One Hardcoded Chart**

**Task 4.1: Install Matplotlib and Seaborn**

- **Start:** `requirements.txt` exists.
- **Action:** Add `matplotlib` and `seaborn` to `requirements.txt`.
- **End:** `requirements.txt` updated.
- **Test:** Run `pip install -r requirements.txt` from the project root.

**Task 4.2: Basic Chart Service (`chart_service.py`) - Generate a Bar Chart Figure**

- **Start:** `matplotlib` installed.
- **Action:** Create `app/services/chart_service.py`:

  ```python
  import matplotlib.pyplot as plt
  from matplotlib.figure import Figure
  import seaborn as sns # For styling

  # Apply a modern, minimal theme once
  # sns.set_theme(style="whitegrid", palette="muted")
  # Or apply per chart if more control is needed.

  def generate_bar_chart_figure(labels, values, title="Bar Chart", xlabel="Categories", ylabel="Values"):
      """Generates a Matplotlib Figure object for a bar chart."""
      fig = Figure(figsize=(5, 4), dpi=100) # Create a Figure
      ax = fig.add_subplot(111) # Add an Axes to the figure

      # Use Seaborn for better aesthetics if desired, or plain Matplotlib
      # sns.barplot(x=labels, y=values, ax=ax, palette="viridis")
      ax.bar(labels, values, color=sns.color_palette("viridis", len(labels)))


      ax.set_title(title)
      ax.set_xlabel(xlabel)
      ax.set_ylabel(ylabel)
      ax.tick_params(axis='x', rotation=45) # Rotate x-labels if they are long
      fig.tight_layout() # Adjust layout to prevent labels from overlapping
      return fig
  ```

  Use code with caution.

- **End:** `app/services/chart_service.py` with `generate_bar_chart_figure`.
- **Test:**
  ```python
  # from app.services import chart_service
  # import matplotlib.pyplot as plt # For showing the plot in test
  # fig = chart_service.generate_bar_chart_figure(["A", "B", "C"], [10, 20, 15], title="Test Chart")
  # plt.show() # This will display the chart in a separate Matplotlib window for testing
  ```
  Use code with caution.

**Task 4.3: `ChartWidget` UI to Display Matplotlib Figure**

- **Start:** `app/services/chart_service.generate_bar_chart_figure` exists.
- **Action:**

  1.  Create `app/ui/widgets/` directory in the project root.
  2.  Create `app/ui/widgets/__init__.py` (empty).
  3.  Create `app/ui/widgets/chart_widget.py`:

      ```python
      import customtkinter as ctk
      from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

      class ChartWidget(ctk.CTkFrame):
          def __init__(self, master, figure):
              super().__init__(master)
              self.figure = figure
              self.canvas = None
              self._draw_chart()

          def _draw_chart(self):
              if self.canvas:
                  self.canvas.get_tk_widget().destroy() # Clear previous chart if any

              self.canvas = FigureCanvasTkAgg(self.figure, master=self)
              self.canvas.draw()
              widget = self.canvas.get_tk_widget()
              widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

          def update_chart(self, new_figure):
              self.figure = new_figure
              self._draw_chart()
      ```

      Use code with caution.

- **End:** `app/ui/widgets/chart_widget.py` created.
- **Test:** Not easily testable in isolation without a figure and a parent window. Will be tested in the next step.

**Task 4.4: Basic `DashboardFrame` UI and Integrate One Chart**

- **Start:** `app/ui/widgets/ChartWidget` and `app/services/chart_service.generate_bar_chart_figure` exist. `app/services/db_service.get_table_names` exists.
- **Action:**

  1.  Create `app/ui/dashboard_frame.py`:

      ```python
      import customtkinter as ctk
      from app.ui.widgets.chart_widget import ChartWidget
      from app.services import chart_service, db_service
      from app.core.app_state import current_app_state
      import seaborn as sns # For styling
      import matplotlib.pyplot as plt


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
      ```

      Use code with caution.

  2.  Integrate `DashboardFrame` into `app/main.py`. For MVP, let's use a TabView.

      ```python
      # Add to imports in app/main.py:
      from app.ui.dashboard_frame import DashboardFrame

      # In App class __init__ (replace the direct packing of converse_frame):
      # ...
      # self.converse_frame = ConverseFrame(self) # Remove direct packing
      # self.converse_frame.pack(fill="both", expand=True, padx=10, pady=10) # Remove

      self.tab_view = ctk.CTkTabview(self)
      self.tab_view.pack(fill="both", expand=True, padx=10, pady=(0,10)) # pady adjusted

      self.tab_view.add("Converse")
      self.tab_view.add("Dashboard")

      self.converse_frame = ConverseFrame(self.tab_view.tab("Converse"))
      self.converse_frame.pack(fill="both", expand=True)

      self.dashboard_frame = DashboardFrame(self.tab_view.tab("Dashboard"))
      self.dashboard_frame.pack(fill="both", expand=True)

      # Call load_dashboard_data initially if connected, or after connection
      # Modify open_connect_dialog in App class:
      # ... (after setting status label for successful connection)
      # if conn:
      #    ...
      #    self.dashboard_frame.load_dashboard_data() # Add this line
      # else:
      #    self.dashboard_frame.load_dashboard_data() # Also call to show "not connected"
      ```

      Use code with caution.
      And to ensure the dashboard attempts to load on startup if already connected (or to show the "not connected" message) and updates the status label correctly:

      ```python
      # In app/main.py, within the App class, modify open_connect_dialog:
      # ...
      # if conn:
      #     current_app_state.db_connection = conn
      #     current_app_state.db_name = details["database"]
      #     self.connection_status_label.configure(text=f"Status: Connected to {details['database']}")
      #     self.dashboard_frame.load_dashboard_data() # Refresh dashboard on new connection
      # else:
      #     self.connection_status_label.configure(text="Status: Connection Failed")
      #     current_app_state.db_connection = None # Ensure it's None
      #     current_app_state.db_name = None
      #     self.dashboard_frame.load_dashboard_data() # To show "not connected" message
      ```

      Use code with caution.

- **End:** `app/ui/dashboard_frame.py` shows a bar chart of table row counts. UI uses TabView.
- **Test:** Run `python app/main.py` from the project root. Connect to DB. Go to "Dashboard" tab. Click "Refresh Dashboard". A bar chart showing row counts for tables in your test DB should appear.

---

This completes a very basic MVP. From here, you can incrementally add features:

- More sophisticated schema parsing in `schema_analyzer.py`.
- Intelligent chart type detection in `chart_service.py`.
- More robust error handling and user feedback.
- Saving/loading connection profiles.
- Improving Gemini prompts and SQL validation.
- Adding more chart types and dashboard widgets.
- Packaging with PyInstaller.
