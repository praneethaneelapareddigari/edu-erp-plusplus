from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import student, course, exam, faculty
from auth import auth_router
from db import init_db

app = FastAPI(title="EduERP++ API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(student.router, prefix="/api", tags=["students"])
app.include_router(course.router, prefix="/api", tags=["courses"])
app.include_router(exam.router, prefix="/api", tags=["exams"])
app.include_router(faculty.router, prefix="/api", tags=["faculties"])

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/", tags=["health"])
async def health():
    return {"status": "ok"}
