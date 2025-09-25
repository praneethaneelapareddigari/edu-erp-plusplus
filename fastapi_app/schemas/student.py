from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    name: str
    roll_no: str
    email: EmailStr

class StudentOut(BaseModel):
    id: int
    name: str
    roll_no: str
    email: EmailStr

    class Config:
        from_attributes = True
