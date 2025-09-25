from sqlalchemy import Column, Integer, String
from ..db import Base

class Faculty(Base):
    __tablename__ = "faculties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dept = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
