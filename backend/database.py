from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "udharbook_db"

# Async MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

# Collections
transactions_collection = database.get_collection("transactions")
notes_collection = database.get_collection("notes")
chat_history_collection = database.get_collection("chat_history")

async def get_database():
    return database