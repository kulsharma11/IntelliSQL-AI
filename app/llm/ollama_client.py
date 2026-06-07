from dotenv import load_dotenv
from langchain_ollama import ChatOllama
import os

load_dotenv()

MODEL_NAME = os.getenv("OLLAMA_MODEL")

llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0
)