import os
from dotenv import load_dotenv

load_dotenv() # Loads variables from .env file into environment

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Basic check
if not GOOGLE_API_KEY:
    print("WARNING: GOOGLE_API_KEY not found in .env file or environment variables.") 