from app.services import nlp_service
# Test 1: Simple text generation
# result = nlp_service.generate_text_with_gemini("Tell me a fun fact about Python programming.")
# print(result)

# Test 2: NL to SQL
sql_query = nlp_service.nl_to_sql_basic("show me all users", "Tables: users (id, name, email)")
print(f"Generated SQL: {sql_query}")