from abc import ABC, abstractmethod
from typing import List
from playwright.sync_api import Page
from src.crawlers.models.job import JobCreate, JobDetail

class BaseCrawler(ABC):
    @abstractmethod
    def get_max_pages(self, page: Page) -> int:
        pass
    
    @abstractmethod
    def get_jobs_from_page(self, page: Page) -> List[JobCreate]:
        pass
    
    @abstractmethod
    def get_job_details(self, page: Page, url: str) -> JobDetail:
        pass