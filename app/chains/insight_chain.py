from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.llm.ollama_client import llm

INSIGHT_PROMPT = ChatPromptTemplate.from_template(
"""
You are a senior business analyst.

Analyze the data below.

Question:
{question}

Data:
{data}

Provide:

1. Key Insights (3-5 bullet points)
2. Business Recommendation

Keep the response concise.
"""
)

insight_chain = (
    INSIGHT_PROMPT
    | llm
    | StrOutputParser()
)