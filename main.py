from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "message": "Study Buddy API is running! "}

@app.get("/notes")
def get_notes():
    return {
        "notes": [
            { "id": 1, "title" : "Calculus", "subject" : "Math"},
            { "id": 2, "title" : "Rizl", "subject" : "History"},
            { "id": 3, "title" : "Photosynthesis", "subject" : "Science"}          
        ]
    }

