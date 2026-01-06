from fastapi import APIRouter, HTTPException
from models import Transaction, TransactionInDB
from database import transactions_collection
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/transactions")
async def create_transaction(transaction: Transaction):
    transaction_dict = transaction.dict()
    result = await transactions_collection.insert_one(transaction_dict)
    transaction_dict["_id"] = str(result.inserted_id)
    return transaction_dict

@router.get("/transactions", response_model=List[dict])
async def get_transactions():
    transactions = []
    async for transaction in transactions_collection.find():
        transaction["_id"] = str(transaction["_id"])
        transactions.append(transaction)
    return transactions

@router.get("/transactions/search")
async def search_transactions(query: str):
    transactions = []
    async for transaction in transactions_collection.find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"relation": {"$regex": query, "$options": "i"}}
        ]
    }):
        transaction["_id"] = str(transaction["_id"])
        transactions.append(transaction)
    return transactions

@router.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: str):
    result = await transactions_collection.delete_one({"_id": ObjectId(transaction_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}

@router.get("/transactions/stats")
async def get_stats():
    transactions = await transactions_collection.find().to_list(length=None)
    
    total_borrowed = sum(t["amount"] for t in transactions if t["type"] == "borrowed")
    total_lent = sum(t["amount"] for t in transactions if t["type"] == "lent")
    net_balance = total_lent - total_borrowed
    
    return {
        "total_borrowed": total_borrowed,
        "total_lent": total_lent,
        "net_balance": net_balance,
        "total_transactions": len(transactions)
    }
    
@router.put("/transactions/{transaction_id}")
async def update_transaction(transaction_id: str, transaction: Transaction):
    if not ObjectId.is_valid(transaction_id):
        raise HTTPException(status_code=400, detail="Invalid transaction ID")

    updated = await transactions_collection.find_one_and_update(
        {"_id": ObjectId(transaction_id)},
        {"$set": transaction.dict()},
        return_document=True
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Transaction not found")

    updated["_id"] = str(updated["_id"])
    return updated
