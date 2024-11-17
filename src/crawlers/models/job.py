from pydantic import BaseModel
from typing import Optional

class JobBase(BaseModel):
    link: str
    status: str = "Open"

class JobCreate(JobBase):
    pass


class JobDetail(JobBase):
    job_title: str
    job_description: Optional[str] = None
    company_name: Optional[str] = None
    company_type: Optional[str] = None
    company_industry: Optional[str] = None
    company_size: Optional[str] = None
    company_country: Optional[str] = None
    company_working_day: Optional[str] = None