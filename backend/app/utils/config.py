import os
from dotenv import load_dotenv

# -------- LOAD ENV --------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
