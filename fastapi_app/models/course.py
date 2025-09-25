from sqlalchemy import Column, Integer, String
from ..db import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False, default=3)
    faculty = Column(String, nullable=True)  # legacy/simple field; association table now supported
