from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os

load_dotenv()

app = FastAPI()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client["study_buddy"]

@app.get("/")
def read_root():
    return { "message": "Study Buddy API is running! "}

@app.get("/notes")
def get_notes():
    notes = []
    for note in db.notes.find():
        note["_id"] = str(note["_id"])
        notes.append(note)
    return { "notes": notes }

@app.post("/notes")
def create_notes(title: str, subject: str, content: str):
    new_note = { 
        "title": title,
        "subject": subject,
        "content": content
    }
    result = db.notes.insert_one(new_note)
    return { "message": "Note saved!" , "id": str(result.inserted_id) }
        
    

