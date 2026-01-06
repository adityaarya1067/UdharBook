from fastapi import APIRouter
from models import ChatMessage, ChatResponse
from database import transactions_collection, notes_collection
from services.rag import build_context

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

router = APIRouter()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a personal finance assistant.

You must answer the user's question using ONLY the provided data.

Rules:
- If the user asks "how much", return ONLY the amount and related details.
- If the user asks "from whom", return ONLY names and amounts borrowed.
- If the user asks "to whom", return ONLY names and amounts lent.
- If the user asks for a summary, then give totals.


Do NOT repeat totals unless explicitly asked.
Do NOT give unnecessary summaries.
Be precise and specific.
"""
    ),
    ("human", "DATA:\n{context}\n\nQUESTION:\n{question}")
])


chain = prompt | llm | StrOutputParser()


@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    try:
        transactions = await transactions_collection.find().to_list(length=None)
        notes = await notes_collection.find().to_list(length=None)

        context = build_context(transactions, notes)

        response = chain.invoke({
            "context": context,
            "question": message.message
        })

        return ChatResponse(response=response)

    except Exception as e:
        print("🔥 LLM ERROR 🔥")
        print(type(e))
        print(str(e))

        return ChatResponse(
            response="⚠️ AI service temporarily unavailable. Please try again later."
        )
