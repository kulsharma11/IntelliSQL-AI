from langchain_core.output_parsers import StrOutputParser

from app.llm.ollama_client import llm
from app.llm.prompts import SQL_PROMPT

sql_chain = (
    SQL_PROMPT
    | llm
    | StrOutputParser()
)