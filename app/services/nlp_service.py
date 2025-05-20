import google.generativeai as genai
from core.config import GOOGLE_API_KEY

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
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