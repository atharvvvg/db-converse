# Project: DB-Converse (Windows Desktop Edition) - Intelligent Database Interaction & Dashboard

## 1. Core Idea & Goals (Unchanged)

- **Connect to MySQL:** Allow users to securely connect to their MySQL databases.
- **Conversational Queries:** Enable users to ask questions in natural language, which are translated into SQL queries using Google Gemini.
- **Intelligent Dashboard:** Automatically generate a summary dashboard with relevant, beautifully styled charts (bar, pie, histogram) based on database schema and data patterns.
- **Main Window:** The primary interface, displaying connection options, the dashboard, and the conversational query interface.

## 2. High-Level Architecture (Desktop Application)

We'll build an integrated desktop application. The UI, business logic, and database interaction logic will all reside within the same Python application process.

```
[User] <--> [Windows Application (UI + Logic)] <--> [MySQL Database]
|
+--> [Google Gemini API (for NLP)]
```

## 3. Technology Stack (Windows Desktop)

- **Language:** Python
- **UI Framework:** **CustomTkinter**
  - _Reasoning:_ CustomTkinter is a Python UI library based on Tkinter that provides modern, customizable widgets with rounded corners and a sleek appearance. It's easier to achieve the desired "modern, minimal, no distraction" styling compared to raw Tkinter, and it's pure Python, making integration seamless.
- **Charting:** **Matplotlib with Seaborn styling**
  - _Reasoning:_
    - **Matplotlib:** Highly versatile, industry-standard, and can be embedded directly into Tkinter/CustomTkinter applications. Offers a vast variety of chart types.
    - **Seaborn:** Built on top of Matplotlib, it provides more aesthetically pleasing default styles and high-level functions for common statistical plots, which will help achieve "beautiful" charts with less manual styling.
    - Compatibility: `matplotlib.pyplot` can be integrated with CustomTkinter using `FigureCanvasTkAgg`.
- **Database Connector:** `mysql-connector-python` (as specified)
- **NLP/LLM:** **Google Gemini API** (via `google-generativeai` Python SDK)
  - _Reasoning:_ User preference for Gemini due to its capabilities and free tier.
- **Data Handling:** Pandas (for schema analysis, data prep for charts)
- **Packaging:** **PyInstaller** (or cx_Freeze)
  - _Reasoning:_ To bundle the Python application and its dependencies into a standalone Windows executable (`.exe`).

## 4. File + Folder Structure (Integrated Desktop App)

```
db-converse-desktop/
├── app/
│ ├── ui/ # CustomTkinter UI elements (windows, frames, custom widgets)
│ │ ├── init.py
│ │ ├── main_window.py # Main application window class
│ │ ├── connect_dialog.py # Dialog for DB connection input
│ │ ├── dashboard_frame.py # Frame to display dashboard charts
│ │ ├── converse_frame.py # Frame for NL query input and results
│ │ └── widgets/ # Custom reusable CTk widgets if any
│ │ └── chart_widget.py # Widget to display a Matplotlib chart
│ ├── services/ # Business logic
│ │ ├── init.py
│ │ ├── db_service.py # Handles DB connections, queries, schema fetching
│ │ ├── nlp_service.py # Handles NL to SQL via Gemini
│ │ ├── chart_service.py # Logic for intelligent chart type detection and Matplotlib generation
│ │ └── schema_analyzer.py # Analyzes DB schema for dashboard suggestions
│ ├── core/ # Core configurations, settings, app-wide state
│ │ ├── init.py
│ │ └── config.py # App settings, (potentially paths to store connection profiles)
│ │ └── app_state.py # Manages shared application state (e.g. current DB connection)
│ ├── assets/ # Static assets (icons, default images)
│ │ └── app_icon.ico
│ ├── utils/ # Utility functions
│ │ ├── init.py
│ │ └── helpers.py
│ ├── init.py
│ └── main.py # Application entry point, initializes CustomTkinter app
│
├── .env.example # Example for Google API Key (loaded by config.py)
├── requirements.txt # Python dependencies
├── build_windows.spec # PyInstaller spec file (generated)
└── README.md
```

## 5. What Each Part Does

**`app/`**

- **`ui/`**: Contains all CustomTkinter related UI code.
  - **`main_window.py`**: Defines the main application window structure (e.g., layout with areas for connection status, dashboard, and conversation). Handles top-level UI events.
  - **`connect_dialog.py`**: A `CTkToplevel` or `CTkInputDialog` for users to input MySQL connection details.
  - **`dashboard_frame.py`**: A `CTkFrame` responsible for fetching and displaying the dashboard charts. It will contain multiple `ChartWidget` instances.
  - **`converse_frame.py`**: A `CTkFrame` with a `CTkTextbox` for NL input and an area (perhaps another `CTkTextbox` or a custom view) to display query results (tabular or simple textual summaries).
  - **`widgets/chart_widget.py`**: A custom `CTkFrame` or `CTkLabel` subclass designed to embed and display a Matplotlib chart figure. This will use `FigureCanvasTkAgg` from `matplotlib.backends.backend_tkagg`.
- **`services/`**: Core application logic, independent of the UI implementation.
  - **`db_service.py`**:
    - Manages database connection using `mysql-connector-python`.
    - Stores the active connection details (securely, if persisting).
    - Executes SQL queries.
    - Fetches database schema.
  - **`nlp_service.py`**:
    - Interfaces with the Google Gemini API (`google-generativeai` SDK).
    - Takes natural language input and database schema (table names, column names/types).
    - Constructs prompts for Gemini optimized for SQL generation.
    - **Crucial:** Implements validation/sanitization for Gemini-generated SQL to prevent injection.
  - **`chart_service.py`**:
    - Receives data (e.g., from `db_service.py` after a query or from `schema_analyzer.py`).
    - **Intelligent Chart Detection:**
      - Analyzes data characteristics (data types, cardinality of categorical data, distribution of numerical data).
      - **Categorical (low unique values):** Suggests Pie chart (for proportions of a whole) or Bar chart (for comparing counts/magnitudes).
      - **Categorical (high unique values):** Suggests Bar chart (showing top N categories).
      - **Numerical (single column):** Suggests Histogram (for frequency distribution).
      - **Numerical over Time-like dimension:** Suggests Line chart (if a date/time or sequence column is present).
      - **Two Numerical Variables:** Scatter plot (for correlation).
    - Uses Matplotlib and Seaborn to generate chart figures. Applies modern, minimal styling (e.g., Seaborn's themes like `seaborn.set_theme(style="whitegrid")` with custom color palettes). Ensures rounded corners where appropriate in chart elements if feasible through Matplotlib's API.
  - **`schema_analyzer.py`**:
    - Fetches schema via `db_service.py`.
    - Identifies key tables, numerical columns, categorical columns, date columns.
    - Suggests initial queries for the dashboard summary (e.g., row counts, sums/averages of important metrics, common value distributions).
- **`core/`**:
  - **`config.py`**: Loads application settings, API keys (e.g., Google API Key from `.env` file or environment variables). Manages paths for storing user-specific connection profiles (e.g., in a JSON file in user's AppData).
  - **`app_state.py`**: A simple module or class to hold global application state, like the current active database connection object (`db_service.connection`), connection status. This helps decouple components.
- **`assets/`**: Contains static files like the application icon.
- **`utils/`**: General helper functions (e.g., for formatting data, error handling).
- **`main.py`**:
  - Initializes CustomTkinter (e.g., `customtkinter.set_appearance_mode("System")`, `customtkinter.set_default_color_theme("blue")`).
  - Creates and runs the main application window (`MainWindow` from `app.ui.main_window`).
  - Sets up the overall application loop.

**External Files:**

- **`.env.example` / `.env`**: Store `GOOGLE_API_KEY`. The `.env` file should be gitignored.
- **`requirements.txt`**: `customtkinter`, `matplotlib`, `seaborn`, `mysql-connector-python`, `pandas`, `python-dotenv`, `google-generativeai`.
- **`build_windows.spec`**: Configuration file for PyInstaller, telling it how to bundle the application.

## 6. Where State Lives & How Services Connect (Desktop Context)

**State Management:**

1.  **Application State (`app/core/app_state.py` & In-Memory Objects):**
    - **DB Connection Object:** The active `mysql.connector` connection object returned by `db_service.py` can be stored in `app_state.py` or passed directly between UI components and services.
    - **Connection Parameters:** User-entered credentials might be temporarily held in the `ConnectDialog`'s state. If "save connection" functionality is added, these (excluding password, or password stored via OS keychain using `keyring` library) could be saved to a local JSON/INI file in a user-specific directory (e.g., `%APPDATA%/DBConverse/profiles.json`).
    - **Dashboard Data:** Chart data (Pandas DataFrames) and Matplotlib figure objects will be held in memory by `DashboardFrame` or its parent.
    - **NL Query Results:** DataFrames or formatted text strings held by `ConverseFrame`.
    - **UI State:** Managed by CustomTkinter widgets themselves (e.g., text in an entry, selected item in a list).
    - **Styling Preferences (Theme):** CustomTkinter handles its own theme state (`customtkinter.set_appearance_mode`).

**Service Connection (Direct Python Calls):**

- **UI <-> Services:** UI components (e.g., `MainWindow`, `DashboardFrame`) will directly import and call methods from the service modules (`db_service`, `nlp_service`, `chart_service`, `schema_analyzer`).
  - _Example:_ `DashboardFrame` might call `chart_service.get_dashboard_charts(app_state.current_connection)`.
- **Services <-> Services:** Services can also call each other.
  - _Example:_ `chart_service` might call `db_service.execute_query(...)` to get data for a chart. `nlp_service` might call `db_service.get_schema_for_llm()`
- **`nlp_service` <-> Google Gemini API:**
  - The `nlp_service.py` will use the `google-generativeai` Python SDK to make HTTP/S requests to the Gemini API. The API key will be managed by `app/core/config.py`.
- **`db_service` <-> MySQL Database:**
  - Uses `mysql-connector-python` to establish a TCP/IP connection to the MySQL server based on user-provided credentials.

## 7. Styling: Modern, Minimal, Rounded Corners, Sleek

- **CustomTkinter:**
  - Set a base theme: `customtkinter.set_appearance_mode("Light")` (or "Dark", "System").
  - Choose a color theme: `customtkinter.set_default_color_theme("blue")` (or other predefined ones like "green", "dark-blue", or create a custom JSON theme file).
  - Widgets like `CTkButton`, `CTkFrame`, `CTkEntry` inherently have rounded corners and modern styling options.
  - Use `CTkFrame` with `corner_radius` for grouping elements.
  - Maintain consistent padding and spacing for a clean, uncluttered look.
- **Charts (Matplotlib/Seaborn):**
  - Use Seaborn's themes: `seaborn.set_theme(style="whitegrid", palette="muted")`. Explore palettes like "pastel", "colorblind" for good aesthetics.
  - Customize Matplotlib:
    - Font choices (ensure they are available on Windows or bundled).
    - Remove unnecessary spines and ticks for a minimal look (`despine()`).
    - Ensure chart background color matches the CustomTkinter theme if embedded directly or use a contrasting neutral.
    - Matplotlib elements don't automatically get "rounded corners" in the same way UI widgets do, but careful design of bars, pie slices, etc., can contribute to a sleek feel.
- **Layout:** Use CustomTkinter's grid and pack managers effectively to create balanced and intuitive layouts. Avoid clutter.

## 8. Workflow Example: Generating Initial Dashboard

1.  **App Start (`main.py`):**
    - Initializes CustomTkinter, sets appearance mode and theme.
    - Creates and displays `MainWindow` instance from `app.ui.main_window`.
2.  **User Interaction (in `MainWindow` or `ConnectDialog`):**
    - User clicks "Connect to Database". `ConnectDialog` opens.
    - User enters MySQL credentials and clicks "Connect".
3.  **Connection Logic (`ConnectDialog` -> `db_service`):**
    - `ConnectDialog` calls `db_service.connect(host, user, password, database)`.
    - `db_service` attempts connection. If successful, stores the connection object in `app.core.app_state.active_connection` and returns success.
    - `ConnectDialog` closes. `MainWindow` is informed of the successful connection (e.g., via a callback or by checking `app_state`).
4.  **Dashboard Generation (`MainWindow` -> `DashboardFrame` -> Services):**
    - `MainWindow` (or a trigger within it) signals `DashboardFrame` to load data.
    - `DashboardFrame` calls `schema_analyzer_service.analyze_current_db_schema(app_state.active_connection)`.
    - `schema_analyzer_service` uses `db_service` to get schema, performs heuristics, and returns analysis (e.g., potential columns/tables for charting).
    - `DashboardFrame` then calls `chart_service.generate_dashboard_charts(analysis_results, app_state.active_connection)`.
5.  **Chart Service Logic (`chart_service.py`):**
    - Based on analysis, constructs and executes summary SQL queries via `db_service.execute_query(...)`.
    - For each query result:
      - Determines the best chart type (pie, bar, histogram).
      - Uses Matplotlib/Seaborn to create a chart `Figure` object. Applies sleek styling.
    - Returns a list of Matplotlib `Figure` objects.
6.  **Displaying Charts (`DashboardFrame` -> `ChartWidget`):**
    - `DashboardFrame` iterates through the returned `Figure` objects.
    - For each figure, it creates an instance of `ChartWidget` (from `app.ui.widgets.chart_widget`).
    - `ChartWidget` uses `FigureCanvasTkAgg(figure, master=self).get_tk_widget()` to create a Tkinter-compatible canvas and displays it.
    - The widgets are arranged in the `DashboardFrame`.

## 9. Security Considerations (Adjusted for Desktop)

- **SQL Injection (from LLM - Gemini):** Still a **MAJOR** risk.
  - The `nlp_service` **must** validate and sanitize SQL from Gemini.
  - Strategies: Restrict to `SELECT`, use a SQL parser library to check syntax and allowed operations, ensure table/column names are from the known schema.
  - Consider using Gemini for query _understanding_ and then constructing the SQL more deterministically if full NL-to-SQL is too risky.
- **Database Credentials:**
  - If storing connection profiles:
    - **Do not store passwords in plain text.**
    - Use the OS keychain/credential manager via Python's `keyring` library. This is the most secure way to store secrets locally.
    - If `keyring` is not used, at least encrypt the file, but key management becomes an issue.
  - Credentials in memory during session should be handled carefully.
- **Gemini API Key:** Store securely (e.g., in `.env` file for development, user provides it, or use environment variables). Do not hardcode in source.
- **Local File Access:** Be mindful if the application writes any other files to disk.
