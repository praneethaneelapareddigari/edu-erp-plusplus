from pydantic import BaseModel

class CourseCreate(BaseModel):
    code: str
    name: str
    credits: int = 3
    faculty: str | None = None

class CourseOut(BaseModel):
    id: int
    code: str
    name: str
    credits: int
    faculty: str | None

    class Config:
        from_attributes = True
