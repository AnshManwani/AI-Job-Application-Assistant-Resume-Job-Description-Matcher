from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Application(Base):
    __tablename__ = "applications"
    __table_args__ = {"extend_existing": True}  # Prevents redefinition errors

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    status = Column(String(100), nullable=False)
    notes = Column(Text)
