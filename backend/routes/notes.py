from fastapi import APIRouter, HTTPException
from models import Note
from database import notes_collection
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/notes")
async def create_note(note: Note):
    note_dict = note.dict()
    result = await notes_collection.insert_one(note_dict)
    note_dict["_id"] = str(result.inserted_id)
    return note_dict

@router.get("/notes", response_model=List[dict])
async def get_notes():
    notes = []
    async for note in notes_collection.find():
        note["_id"] = str(note["_id"])
        notes.append(note)
    return notes

@router.delete("/notes/{note_id}")
async def delete_note(note_id: str):
    result = await notes_collection.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}