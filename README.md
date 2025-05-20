# DB-Converse: Intelligent Database Interaction & Dashboard

## 1. Why DB-Converse? (Purpose)

DB-Converse is a desktop application designed to simplify interactions with MySQL databases. Many users, including analysts, developers, and data scientists, often need to quickly query databases or get a visual summary of their data without writing complex SQL or setting up elaborate business intelligence tools. DB-Converse aims to bridge this gap by:

- **Lowering the barrier to data access:** Allowing users to ask questions in natural language.
- **Providing quick insights:** Automatically generating a basic dashboard with key data summaries.
- **Offering a user-friendly interface:** Making database connections and data exploration straightforward.

The core idea is to provide an intelligent assistant for your database, making data more accessible and actionable for a wider range of users.

## 2. Features (MVP)

- **MySQL Database Connection:**
  - Securely connect to MySQL databases using a simple dialog (host, user, password, database name).
  - Connection status is displayed in the UI.
  - Connections are properly closed when the application exits.
- **Conversational Queries (NL-to-SQL):**
  - Input natural language questions (e.g., "show all users", "list products with price over 50").
  - Utilizes Google Gemini API to translate natural language into SQL queries.
  - Displays the generated SQL query in the UI.
  - Executes the generated SQL (currently `SELECT` and `SHOW` statements for MVP) against the connected database.
  - Displays query results (or errors) in a text area.
- **Basic Dashboard:**
  - A dedicated "Dashboard" tab.
  - Automatically generates and displays a bar chart showing row counts for each table in the connected database upon refresh.
  - Displays appropriate messages if not connected to a database, or if no tables/data are found.
- **User Interface:**
  - Built with CustomTkinter for a modern look and feel.
  - Tabbed interface for "Converse" (NLQ) and "Dashboard" views.
  - Responsive UI elements for input and output.
- **Configuration:**
  - Uses a `.env` file for managing the Google Gemini API Key.

## 3. Technology Stack

- **Language:** Python 3.9+
- **UI Framework:** CustomTkinter
- **Charting:** Matplotlib with Seaborn styling
- **Database Connector:** `mysql-connector-python`
- **NLP/LLM:** Google Gemini API (via `google-generativeai` Python SDK)
- **Data Handling:** Pandas (for query results and data preparation for charts)
- **Environment Management:** `python-dotenv`

(For a more detailed architectural overview, see `architecture.md`)

## 4. Project Structure

```
db-converse/
├── app/
│   ├── ui/                 # CustomTkinter UI elements
│   │   ├── widgets/        # Reusable UI widgets (e.g., ChartWidget)
│   │   ├── __init__.py
│   │   ├── connect_dialog.py
│   │   ├── converse_frame.py
│   │   └── dashboard_frame.py
│   ├── services/           # Business logic
│   │   ├── __init__.py
│   │   ├── db_service.py     # Database connection, schema, query execution
│   │   ├── nlp_service.py    # Gemini integration for NL-to-SQL
│   │   └── chart_service.py  # Chart generation
│   ├── core/               # Core configuration, app state
│   │   ├── __init__.py
│   │   ├── config.py         # API key loading
│   │   └── app_state.py      # Shared application state (e.g., DB connection)
│   ├── __init__.py
│   └── main.py             # Application entry point
├── .venv/                  # Python virtual environment
├── .env.example            # Example for API Key configuration
├── .gitignore
├── architecture.md         # Detailed architecture document
├── README.md               # This file
├── requirements.txt        # Python dependencies
└── tasks.md                # Project tasks (completed for MVP)
```

## 5. Setup and Installation

1.  **Clone the repository (if applicable) or ensure you have all project files.**
2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure API Key:**
    - Create a `.env` file in the project root by copying `.env.example`:
      ```
      GOOGLE_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
      ```
    - Replace `"YOUR_ACTUAL_GEMINI_API_KEY"` with your valid Google Gemini API key.

## 6. How to Run

After completing the setup:

1.  Ensure your virtual environment is activated.
2.  Run the main application script from the project root:
    ```bash
    python app/main.py
    ```
3.  The application window will appear. Use the "Connect to Database" button to connect to your MySQL instance.
4.  Explore the "Converse" and "Dashboard" tabs.

## 7. Future Improvements

This MVP provides a solid foundation. Future enhancements could include:

- **More Sophisticated Schema Analysis:**
  - Move beyond just table names to include column names and types in the schema information provided to the LLM for better SQL generation.
  - Implement a dedicated `schema_analyzer.py` for more detailed analysis.
- **Intelligent Chart Generation:**
  - In `chart_service.py`, detect appropriate chart types (pie, bar, histogram, line) based on data characteristics (e.g., categorical vs. numerical data, cardinality).
  - Allow users to request specific chart types or have the dashboard suggest multiple relevant charts.
- **Enhanced NL-to-SQL:**
  - Improve Gemini prompts for more complex queries and better SQL accuracy.
  - Implement more robust SQL validation and sanitization beyond the current `SELECT`/`SHOW` check.
  - Handle a wider range of SQL dialects if support for other databases is added.
- **Dashboard Customization:**
  - Allow users to select which data/tables to include in the dashboard.
  - Enable saving and loading of dashboard configurations.
  - Add more chart types and dashboard widgets (e.g., key performance indicators (KPIs), data tables).
- **Connection Management:**
  - Save and load database connection profiles.
  - Encrypt stored credentials (e.g., using the `keyring` library).
- **User Experience (UX) and UI Polish:**
  - More detailed error messages and user feedback.
  - Loading indicators for long-running operations.
  - Refine UI layouts and styling.
- **Advanced Features:**
  - Support for other database systems (e.g., PostgreSQL, SQLite).
  - Data export capabilities (e.g., export query results to CSV).
  - User accounts or profiles.
- **Packaging:**
  - Bundle the application into a standalone executable (e.g., using PyInstaller) for easier distribution on Windows.
