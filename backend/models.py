from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class Transaction(BaseModel):
    name: str
    amount: float
    type: Literal["borrowed", "lent"]
    relation: str
    date: str

class TransactionInDB(Transaction):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)

class Note(BaseModel):
    title: str
    content: str
    category: str = "general"

class NoteInDB(Note):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str