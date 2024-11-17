import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from src.database.models import Base, Job
from src.crawlers.models.job import JobCreate, JobDetail
from src.utils.logger import get_logger


load_dotenv()

logger = get_logger(__name__)

class DatabaseManager:
    def __init__(self):
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL not found in environment variables")
            
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def add_job(self, job: JobCreate) -> bool:
        job_data = job.model_dump()
        session = self.SessionLocal()
        try:
            new_job = Job(**job_data)
            session.add(new_job)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False
        except Exception as e:
            logger.error(f"Error adding job: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()

    def get_jobs_for_update(self, limit: int = 100) -> list:
        session = self.SessionLocal()
        try:
            
            jobs = session.query(Job)\
                .filter(Job.status == 'Open')\
                .filter(Job.job_title == None)\
                .limit(limit)\
                .all()
            return jobs
        finally:
            session.close()

    def update_job(self, link: str, job_details: JobDetail) -> bool:
        job_data = job_details.model_dump()
        session = self.SessionLocal()
        try:
            job = session.query(Job).filter(Job.link == link).first()
            if job:
                for key, value in job_data.items():
                    setattr(job, key, value)
                session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating job: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()
