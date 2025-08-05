# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# llm = ChatGoogleGenerativeAI(
#     model="gemini-pro",  # ✅ Use the correct model for LangChain + Gemini AI Studio
#     google_api_key=GEMINI_API_KEY
# )

#groq
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SMTP_KEY = os.getenv("SMTP_KEY")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama3-70b-8192",  # ✅ Recommended supported model
    temperature=0.3  # Add temperature to reduce hallucinations
)


