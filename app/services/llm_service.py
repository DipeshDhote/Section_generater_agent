from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from app.utils.logger import AppLogger

logger = AppLogger(__name__).get_logger()

load_dotenv()

# =====================================================
# Load LLM
# ======================================================
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3)



# llm = ChatMistralAI(
#     model="mistral-large-latest",
#     temperature=0.3,
# )

# llm = ChatGroq(
#     model="llama-3.1-70b-versatile",
#     temperature=0.4,
# )
