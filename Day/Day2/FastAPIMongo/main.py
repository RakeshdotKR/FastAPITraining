from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import AsyncMongoClient
from bson import ObjectId  #pip install bson (to be executed)

app = FastAPI()

# --------------------------------------------------
# MongoDB Connection
# --------------------------------------------------

client = AsyncMongoClient("mongodb://localhost:27017/")

db = client["college"]

students_collection = db["student"]

# --------------------------------------------------
# Pydantic Model
# --------------------------------------------------

class Student(BaseModel):
    name: str
    age: int
    course: str
    marks: float


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
async def home():
    return {
        "message": "FastAPI + MongoDB CRUD API"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health():
    try:
        result = await db.command("ping")

        return {
            "mongodb": "connected",
            "ping": result["ok"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"MongoDB connection failed: {str(e)}"
        )


# --------------------------------------------------
# CREATE
# POST /students
# --------------------------------------------------

@app.post("/students")
async def create_student(student: Student):

    result = await students_collection.insert_one(
        student.model_dump()
    )

    return {
        "message": "Student created",
        "id": str(result.inserted_id)
    }


# --------------------------------------------------
# READ ALL
# GET /students
# --------------------------------------------------

@app.get("/students")
async def get_students():

    students = []

    async for student in students_collection.find():
        student["_id"] = str(student["_id"])
        students.append(student)

    return students


# --------------------------------------------------
# READ ONE
# GET /students/{student_id}
# --------------------------------------------------

@app.get("/students/{student_id}")
async def get_student(student_id: str):

    # Validate ObjectId
    try:
        object_id = ObjectId(student_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid student ID"
        )

    # Find student
    student = await students_collection.find_one(
        {"_id": object_id}
    )

    # Student not found
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Convert ObjectId to string
    student["_id"] = str(student["_id"])

    return student


# --------------------------------------------------
# UPDATE
# PUT /students/{student_id}
# --------------------------------------------------

@app.put("/students/{student_id}")
async def update_student(
    student_id: str,
    student: Student
):

    # Validate ObjectId
    try:
        object_id = ObjectId(student_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid student ID"
        )

    # Update student
    result = await students_collection.update_one(
        {"_id": object_id},
        {
            "$set": student.model_dump()
        }
    )

    # Student not found
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student updated"
    }


# --------------------------------------------------
# DELETE
# DELETE /students/{student_id}
# --------------------------------------------------

@app.delete("/students/{student_id}")
async def delete_student(student_id: str):

    # Validate ObjectId
    try:
        object_id = ObjectId(student_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid student ID"
        )

    # Delete student
    result = await students_collection.delete_one(
        {"_id": object_id}
    )

    # Student not found
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted"
    }
