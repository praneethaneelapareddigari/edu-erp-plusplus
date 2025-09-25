from sqlalchemy import Column, Integer, String, Date
from ..db import Base

class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    course_code = Column(String, nullable=False)
    results_json = Column(String, nullable=True)  # simple JSON string for bulk results
