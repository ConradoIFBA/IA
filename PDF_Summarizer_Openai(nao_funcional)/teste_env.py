import os
from dotenv import load_dotenv

load_dotenv()

print("API Key carregada:", os.getenv("OPENAI_API_KEY"))
