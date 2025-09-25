from pydantic import BaseModel, EmailStr

class FacultyCreate(BaseModel):
    name: str
    dept: str | None = None
    email: EmailStr

class FacultyOut(BaseModel):
    id: int
    name: str
    dept: str | None
    email: EmailStr
    class Config:
        from_attributes = True
