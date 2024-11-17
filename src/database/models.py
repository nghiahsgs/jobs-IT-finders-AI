from sqlalchemy import Boolean, Column, String, Text, Enum, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(767), unique=True, nullable=False)
    job_title = Column(Text)
    job_description = Column(Text)
    company_name = Column(Text)
    company_type = Column(String(255))
    company_industry = Column(String(255))
    company_size = Column(String(255))
    company_country = Column(String(255))
    company_working_day = Column(String(255))
    status = Column(Enum('Open', 'Close'), default='Open')
