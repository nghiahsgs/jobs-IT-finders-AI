from typing import List, Dict, Any
from langchain_core.documents import Document
from src.database.operations import DatabaseManager
from src.database.models import Job
from src.utils.logger import get_logger

logger = get_logger(__name__)

class JobDocumentLoader:
    def __init__(self):
        self.db = DatabaseManager()
    
    def _clean_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Clean metadata by removing None values and converting to basic types"""
        cleaned = {}
        for key, value in metadata.items():
            if value is not None:
                # Convert to basic types
                if isinstance(value, (str, int, float, bool)):
                    cleaned[key] = value
                else:
                    cleaned[key] = str(value)
        return cleaned
    
    def load_documents(self) -> List[Document]:
        """Load jobs from database and convert to Langchain Documents"""
        session = self.db.SessionLocal()
        try:
            jobs = session.query(Job).all()
            documents = []
            
            # Thêm document tổng quan
            total_open = session.query(Job).filter(Job.status == 'Open').count()
            summary_content = f"""
            Thống kê tổng quan:
            - Tổng số job đang open: {total_open}
            """
            summary_doc = Document(
                page_content=summary_content,
                metadata={"type": "summary"}
            )
            documents.append(summary_doc)
            
            for job in jobs:
                # Combine relevant fields into content
                content = f"""
                Job Title: {job.job_title or 'N/A'}
                Company: {job.company_name or 'N/A'}
                Description: {job.job_description or 'N/A'}
                Company Type: {job.company_type or 'N/A'}
                Industry: {job.company_industry or 'N/A'}
                Company Size: {job.company_size or 'N/A'}
                Country: {job.company_country or 'N/A'}
                Working Days: {job.company_working_day or 'N/A'}
                Status: {job.status or 'N/A'}
                """
                
                # Create metadata và lọc bỏ các giá trị None
                metadata = self._clean_metadata({
                    "job_id": job.id,
                    "link": job.link,
                    "company_name": job.company_name,
                    "status": job.status
                })
                
                # Create Document
                doc = Document(
                    page_content=content,
                    metadata=metadata
                )
                documents.append(doc)
                
            return documents
            
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            raise
        finally:
            session.close()