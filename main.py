from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from bson import ObjectId
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from auth import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from google import genai
from datetime import datetime, timedelta
import os


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client["study_buddy"]

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class ChatCreate(BaseModel):
    title: str = "New Chat"

class MessageAdd(BaseModel):
    question: str
    note_id: str = None

class ChatTitleUpdate(BaseModel):
    title: str

class ChatMessage(BaseModel):
    question: str


class LibraryCreate(BaseModel):
    title: str = "New Library"

class SourceAdd(BaseModel): 
    type: str
    content: str 
    label: str =""

class LibraryChatMessage(BaseModel):
    question: str
    selected_sources: list[str]


class FlashcardSetCreate(BaseModel):
    title: str = "New Flashcard Set"

class FlashcardSetUpdate(BaseModel):
    content:str

class AssignmentCreate(BaseModel):
    title: str = "New Assignment"

class AssignmentSourceAdd(BaseModel):
    type: str
    content: str
    label: str = ""

class AssignmentChatMessage(BaseModel):
    question: str
    selected_sources: list[str]
    image_base64: str = None

class QuizGenerateRequest(BaseModel):
    notes:str

class AnswerSubmit(BaseModel):
    question_index: int 
    user_answer: str

@app.post("/register")
async def register(user: UserRegister):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already Registered")
    
    hashed = hash_password(user.password)
    new_user = {
        "email": user.email,
        "password": hashed
    }
    await db.users.insert_one(new_user)
    return {"message" : "User registered succesfully"}

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_user = await db.users.find_one({"email": email})
    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return db_user

@app.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"email": current_user["email"]}


@app.get("/notes")
async def get_notes(current_user: dict = Depends(get_current_user)):
    notes = []
    async for note in db.notes.find({"user_id": current_user["_id"]}):
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])
        notes.append(note)
    return { "notes": notes }

class NoteCreate(BaseModel):
    title: str
    subject: str
    content: str
   
@app.post("/notes")
async def create_note(note: NoteCreate, current_user: dict = Depends(get_current_user)):
    new_note = {
        "user_id": current_user["_id"],
        "title": note.title,
        "subject": note.subject,
        "content": note.content
    }
    result = await db.notes.insert_one(new_note)
    return {"message": "Note saved!", "id": str(result.inserted_id)}

class AskQuestion(BaseModel):
    note_id: str
    question: str

@app.post("/ask")
async def ask_question(note: AskQuestion, current_user : dict = Depends(get_current_user)):
    db_note = await db.notes.find_one({"_id": ObjectId(note.note_id)})
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if db_note["user_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail ="Not allowed")
    
    prompt = f"""
    You are a helpful study buddy for Filipino students.
    Always answer in Taglish (mix of Tagalog and English).
    Make your explanation easy to understand.

    Here is the student's note:
    {db_note["content"]}

    Question: {note.question}
    """

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        answer = response.text
        total_tokens = response.usage_metadata.prompt_token_count + response.usage_metadata.candidate_token_count
        return {"answer": answer, "tokens_used": total_tokens}
    except Exception as e:
        print(f"AI Error: {e}") 
        raise HTTPException(status_code=503, detail="AI service unavailable.Please try again.")

@app.post("/chats")
async def create_chat(chat: ChatCreate, current_user: dict = Depends(get_current_user)):
    new_chat = {
        "user_id": current_user["_id"],
        "title": chat.title,
        "messages": [],
        "created_at": datetime.utcnow()
    }
    result = await db.chats.insert_one(new_chat)
    return {"id": str(result.inserted_id), "title": chat.title}

@app.get("/chats")
async def get_chats(current_user: dict = Depends(get_current_user)):
    chats = []
    async for chat in db.chats.find({"user_id": current_user["_id"]}).sort("created_at", -1):
        chat["_id"] = str(chat["_id"])
        chat["user_id"] = str(chat["user_id"])
        chats.append(chat)
    return {"chats": chats}
    
@app.get("/chats/{chat_id}")
async def get_chat(chat_id: str, current_user: dict = Depends(get_current_user)):
    chat = await db.chats.find_one({"_id": ObjectId(chat_id)})
    if not chat: 
        raise HTTPException(status_code=404, detail="Chat not found")
    chat["_id"] = str(chat["_id"])
    chat["user_id"] = str(chat["user_id"])
    return chat

@app.post("/chats/{chat_id}/ask")
async def chat_ask(chat_id: str, message: ChatMessage, current_user: dict = Depends(get_current_user)):
    chat = await db.chats.find_one({"_id": ObjectId(chat_id)})
    if not chat: 
        raise HTTPException(status_code=404, detail="Chat not found")
    
    prompt =f"""
    You are Liwanag, a helpful AI study buddy for Filipino students.
    Always answer in Taglish (mix of Tagalog and English).
    Make your explanation easy to understand.

    Question: {message.question}
    """
    try:
        response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
        )
        answer = response.text
        total_tokens = response.usage_metadata.prompt_token_count + response.usage_metadata.candidate_token_count
   
        await db.chats.update_one(
            {"_id": ObjectId(chat_id)},
            {"$push": {"messages": {
                "question": message.question,
                "answer": answer,
                "created_at": datetime.utcnow()
            }}}
        )

        return {"answer": answer,"tokens_used": total_tokens }
    except Exception as e:
        print(f"AI Error: {e}") 
        raise HTTPException(status_code=503, detail="AI service unavailable. Please try again later.")


@app.patch("/chats/{chat_id}/title")
async def update_chat_title(chat_id: str, update: ChatTitleUpdate, current_user: dict = Depends(get_current_user)):
    await db.chats.update_one(
        {"_id": ObjectId(chat_id)},
        {"$set": {"title": update.title}}
    )
    return {"message": "Title updated"}

@app.delete("/chats/{chat_id}")
async def delete_chat(chat_id: str, current_user: dict = Depends(get_current_user)):
    await db.chats.delete_one({"_id": ObjectId(chat_id)})
    return {"message": "Chat deleted"}

#Upload Rest
@app.post("/library")
async def create_library(library: LibraryCreate, current_user: dict = Depends(get_current_user)):
    new_library = {
        "user_id": current_user["_id"],
        "title": library.title,
        "sources": [],
        "created_at": datetime.utcnow()
    }
    result = await db.library.insert_one(new_library)
    return {"id": str(result.inserted_id), "title": library.title}

@app.get("/library")
async def get_libraries(current_user: dict = Depends(get_current_user)):
    libraries = []
    async for lib in db.library.find({"user_id": current_user["_id"]}).sort("created_at", -1):
        lib["_id"] = str(lib["_id"])
        lib["user_id"] = str(lib["user_id"])
        libraries.append(lib)
    return {"libraries": libraries}

@app.get("/library/{lib_id}")
async def get_library(lib_id: str, current_user: dict = Depends(get_current_user)):
    lib = await db.library.find_one({"_id": ObjectId(lib_id)})
    if not lib: 
        raise HTTPException(status_code=404, detail='Library not found')
    lib["_id"] = str(lib["_id"])
    lib["user_id"] = str(lib["user_id"])
    return lib

@app.post("/library/{lib_id}/sources")
async def get_source(lib_id: str, source: SourceAdd, current_user: dict = Depends(get_current_user)):
    new_source = {
        "id": str(ObjectId()),
        "type": source.type,
        "content": source.content,
        "label" : source.label or source.content[:50]
    }
    await db.library.update_one(
        {"_id": ObjectId(lib_id)},
        {"$push" : {"sources": new_source}}
    )
    return {"source": new_source}

@app.delete("/library/{lib_id}/sources/{source_id}")
async def delete_source(lib_id: str, source_id: str, current_user: dict = Depends(get_current_user)):
    await db.library.update_one(
        {"_id": ObjectId(lib_id)},
        {"$pull": {"sources": {"id": source_id}}}
    )
    return {"message": "Source deleted"}

@app.delete("/library/{lib_id}")
async def delete_library(lib_id: str, current_user: dict = Depends(get_current_user)):
    await db.library.delete_one({"_id": ObjectId(lib_id)})
    return {"message": "Library deleted"}

@app.post("/library/{lib_id}/chat")
async def library_chat(lib_id: str, message: LibraryChatMessage, current_user: dict = Depends(get_current_user)):
    lib = await db.library.find_one({"_id": ObjectId(lib_id)})
    if not lib: 
        raise HTTPException(status_code=404, detail="Library not found")
    
    selected = [s for s in lib["sources"] if s["id"] in message.selected_sources]
    sources_text = "\n\n".join([f"Source ({s['type']}): {s['content']}" for s in selected])

    prompt = f"""
    You are Liwanag, a helpful AI study buddy for Filipino students.
    Answer ONLY based on the sources provided below. 
    Always answer in Taglish (mix of Tagalog and English).
    If the answer is not in the sources, say "Hindi ko makita sa sources na ibinigay mo."

    Sources:
    {sources_text}

    Question: {message.question}
    """
    
    try: 
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        answer = response.text
        return {"answer": answer}
    except Exception as e: 
        print(f"AI Error: {e}")
        raise HTTPException(status_code=503, detail="AI service unavailable. Please try again later.")
#FlashCARD REST API

@app.post("/flashcards")
async def create_flashcard_set(flashcard: FlashcardSetCreate, current_user: dict = Depends(get_current_user)):
    new_set = {
        "user_id": current_user["_id"],
        "title": flashcard.title,
        "content": "",
        "cards": [],
        "created_at": datetime.utcnow()
    }
    result = await db.flashcards.insert_one(new_set)
    return {"id": str(result.inserted_id), "title": flashcard.title}

@app.get("/flashcards")
async def get_flashcard_sets(current_user: dict = Depends(get_current_user)):
    sets = []
    async for fs in db.flashcards.find({"user_id": current_user["_id"]}).sort("created_at", -1):
        fs["_id"] = str(fs["_id"])
        fs["user_id"] = str(fs["user_id"])
        sets.append(fs)
    return {"flashcards": sets}

@app.get("/flashcards/{set_id}")
async def get_flashcard_set(set_id: str, current_user: dict = Depends(get_current_user)):
    fs = await db.flashcards.find_one({"_id": ObjectId(set_id)})
    if not fs:
        raise HTTPException(status_code=404, detail="Flashcard set not found")
    fs["_id"] = str(fs["_id"])
    fs["user_id"] = str(fs["user_id"])
    return fs

@app.delete("/flashcards/{set_id}")
async def delete_flashcard_set(set_id: str, current_user: dict = Depends(get_current_user)):
    await db.flashcards.delete_one({"_id": ObjectId(set_id)})
    return { "message": "Flashcard set deleted"}

@app.post("/flashcards/{set_id}/generate")
async def  generate_flashcards(set_id: str, update: FlashcardSetUpdate, current_user: dict = Depends(get_current_user)):
    prompt = f"""
    You are a helpful study buddy for Filipino students.
    Based on the following notes, generate 10 flashcard questions and answers.
    Respond ONLY in this exact JSON format, no other text:
    [
        {{"question": "...", "answer": "..."}}
        {{"question": "...", "answer": "..."}}
    ]

    Notes:
    {update.content}
    """
    try:
        response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
        import json
        cards = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        await db.flashcards.update_one(
            {"_id": ObjectId(set_id)},
            {"$set": {"content": update.content, "cards": cards}}
        )
        return {"cards": cards}
    except Exception as e:
        print(f"AI Error: {e}") 
        raise HTTPException(status_code=503, detail="AI service unavailable. Please try again later.")

# ASSIGNMENT REST API

@app.post("/assignments")
async def create_assignment(assignment: AssignmentCreate, current_user: dict = Depends(get_current_user)):
    new_assignment = {
        "user_id": current_user["_id"],
        "title": assignment.title,
        "sources": [],
        "created_at": datetime.utcnow()
    }
    result = await db.assignments.insert_one(new_assignment)
    return {"id": str(result.inserted_id), "title": assignment.title}

@app.get("/assignments")
async def get_assignments(current_user: dict = Depends(get_current_user)):
    assignments = []
    async for a in db.assignments.find({"user_id": current_user["_id"]}).sort("created_at", -1):
        a["_id"] = str(a["_id"])
        a["user_id"] = str(a["user_id"])
        assignments.append(a)
    return {"assignments": assignments}

@app.get("/assignments/{assignment_id}")
async def get_assignment(assignment_id: str, current_user: dict = Depends(get_current_user)):
    a = await db.assignments.find_one({"_id": ObjectId(assignment_id)})
    if not a:
        raise HTTPException(status_code=404, detail="Assignment not found")
    a["_id"] = str(a["_id"])
    a["user_id"] = str(a["user_id"])
    return a

@app.post("/assignments/{assignment_id}/sources")
async def add_assignment_source(assignment_id: str, source: AssignmentSourceAdd, current_user: dict = Depends(get_current_user)):
    new_source = {
        "id": str(ObjectId()),
        "type": source.type,
        "content": source.content,
        "label": source.label or source.content[:50]
    }
    await db.assignments.update_one(
        {"_id": ObjectId(assignment_id)},
        {"$push": {"sources": new_source}}
    )
    return {"source": new_source}

@app.delete("/assignments/{assignment_id}/sources/{source_id}")
async def delete_assignment_source(assignment_id: str, source_id: str, current_user: dict = Depends(get_current_user)):
    await db.assignments.update_one(
        {"_id": ObjectId(assignment_id)},
        {"$pull": {"sources": {"id": source_id}}}
    )
    return {"message": "Source deleted"}

@app.delete("/assignments/{assignment_id}")
async def delete_assignment(assignment_id: str, current_user: dict = Depends(get_current_user)):
    await db.assignments.delete_one({"_id": ObjectId(assignment_id)})
    return {"message": "Assignment deleted"}

@app.post("/assignments/{assignment_id}/chat")
async def assignment_chat(assignment_id: str, message: AssignmentChatMessage, current_user: dict = Depends(get_current_user)):
    a = await db.assignments.find_one({"_id": ObjectId(assignment_id)})
    if not a:
        raise HTTPException(status_code=404, detail="Assignment not found")

    selected = [s for s in a["sources"] if s["id"] in message.selected_sources]
    sources_text = "\n\n".join([f"Source ({s['type']}): {s['content']}" for s in selected if s["type"] == "text"])

    prompt = f"""
    You are Liwanag, a helpful AI study buddy for Filipino students.
    Help the student understand and complete their assignment.
    Always answer in Taglish (mix of Tagalog and English).

    Sources:
    {sources_text}

    Question: {message.question}
    """

    try:
        contents = [prompt]
        if message.image_base64:
            import base64
            contents = [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": message.image_base64
                            }
                        }
                    ]
                }
            ]

        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )
        answer = response.text
        return {"answer": answer}
    except Exception as e:
        print(f"AI Error: {e}")
        raise HTTPException(status_code=503, detail="AI service unavailable. Please try again later.")
  
# QUIZ REST API

@app.post("/quizzes/generate")
async def generate_quiz(request: QuizGenerateRequest, current_user: dict = Depends(get_current_user)):
    prompt = f"""
    You are a quiz generator for Filipino students.
    Based on the notes below, generate as many multiple choice questions as the content supports.
    Minimum 5 questions, maximum 20 questions.
    If the notes are detailed and long, generate more questions.
    If the notes are short, generate fewer but still meaningful questions.
    Always write all questions and choices in English.
    Respond ONLY in this exact JSON format, no explanation, no markdown, no backticks:
    [
        {{
            "question": "...",
            "choices": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
            "answer": "A"
        }}
    ]

    Notes:
    {request.notes}
    """
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        import json
        questions = json.loads(response.text.strip().replace("```json", "").replace("```", ""))

        title_prompt = f"Give a short 4-6 word title for a quiz about these notes. Return only the title, nothing else:\n{request.notes[:300]}"
        title_response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=title_prompt
        )
        title = title_response.text.strip()

        quiz_doc = {
            "user_id": current_user["_id"],
            "title": title,
            "questions": questions,
            "created_at": datetime.utcnow()
        }
        result = await db.quizzes.insert_one(quiz_doc)

        safe_questions = [
            {"question": q["question"], "choices": q["choices"]}
            for q in questions
        ]

        return {
            "id": str(result.inserted_id),
            "title": title,
            "questions": safe_questions
        }
    except Exception as e:
        print(f"AI Error: {e}")
        raise HTTPException(status_code=503, detail="AI service unavailable. Please try again later.")


@app.get("/quizzes")
async def get_quizzes(current_user: dict = Depends(get_current_user)):
    quizzes = []
    async for q in db.quizzes.find({"user_id": current_user["_id"]}).sort("created_at", -1):
        quizzes.append({"id": str(q["_id"]), "title": q["title"]})
    return {"quizzes": quizzes}

@app.post("/quizzes")
async def create_quiz(current_user: dict = Depends(get_current_user)):
    quiz_doc = {
        "user_id": current_user["_id"],
        "title": "New Quiz",
        "questions": [],
        "created_at": datetime.utcnow()
    }
    result = await db.quizzes.insert_one(quiz_doc)
    return {"id": str(result.inserted_id), "title": "New Quiz"}

@app.post("/quizzes/{quiz_id}/submit-answer")
async def submit_answer(quiz_id: str, request: AnswerSubmit, current_user: dict = Depends(get_current_user)):
    quiz = await db.quizzes.find_one({
        "_id": ObjectId(quiz_id),
        "user_id": current_user["_id"]
    })
    if not quiz:    
        raise HTTPException(status_code=404, detail="Quiz not found")

    correct_answer = quiz["questions"][request.question_index]["answer"]
    is_correct = request.user_answer == correct_answer

    return {
        "is_correct": is_correct,
        "correct_answer": correct_answer
    }

@app.get("/quizzes/{quiz_id}")
async def get_quiz(quiz_id: str, current_user: dict = Depends(get_current_user)):
    quiz = await db.quizzes.find_one({
        "_id": ObjectId(quiz_id),
        "user_id": current_user["_id"]
    })
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    safe_questions = [
        {"question": q["question"], "choices": q["choices"]}
        for q in quiz["questions"]
    ]
    return {
        "id": str(quiz["_id"]),
        "title": quiz["title"],
        "questions": safe_questions
    }


@app.delete("/quizzes/{quiz_id}")
async def delete_quiz(quiz_id: str, current_user: dict = Depends(get_current_user)):
    await db.quizzes.delete_one({
        "_id": ObjectId(quiz_id),
        "user_id": current_user["_id"]
    })
    return {"message": "Quiz deleted"}

@app.get("/activity")
async def get_activity(current_user: dict = Depends(get_current_user)):
    today = datetime.utcnow()
    days = []
    day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    for i in range(6, -1, 1):
        day = today - timedelta(days=i)
        start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end = day.replace(hour=23, minute=59, second=59, microsecond=999999)

        collections = [db.chats, db.library, db.flashcards, db.assignments, db.quizzes]
        count = 0
        for col in collections:
            count += await col.count_documents({
                "user_id": current_user["_id"],
                "created_at": {"$gte": start, "$lte": end}
            })

        days.append({
            "day": day_names[day.weekday() % 7],
            "date": day.strftime("%Y-%m-%d"),
            "count": count,
            "isToday": i == 0
        })

    return {"activity": days}