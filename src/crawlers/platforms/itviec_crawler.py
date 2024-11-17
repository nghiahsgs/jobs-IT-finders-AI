import time
import random
from typing import List, Dict, Any
from playwright.sync_api import Page

from src.crawlers.models.job import JobCreate, JobDetail
from src.crawlers.base.base_crawler import BaseCrawler
from src.utils.logger import get_logger


logger = get_logger(__name__)

class ITViecCrawler(BaseCrawler):
    BASE_URL = "https://itviec.com/it-jobs/ha-noi"
    
    def __init__(self):
        self.delay_between_requests = (1, 3)  # Random delay between requests
        self.delay_between_pages = (3, 7)     # Random delay between pages
    
    def get_max_pages(self, page: Page) -> int:
        try:
            pagination_elements = page.query_selector_all(
                '.page a[data-action="ajax:success->search--pagination#paginate"]'
            )
            page_numbers = []
            for element in pagination_elements:
                text = element.text_content().strip()
                try:
                    number = int(text)
                    page_numbers.append(number)
                except ValueError:
                    continue
            
            return max(page_numbers) if page_numbers else 1
        except Exception as e:
            logger.error(f"Error getting max pages: {str(e)}")
            return 1

    def get_jobs_from_page(self, page: Page) -> List[JobCreate]:
        jobs = []
        try:
            job_elements = page.query_selector_all(
                'h3[data-search--job-selection-target="jobTitle"]'
            )
            
            for job in job_elements:
                job_url = job.get_attribute('data-url')
                
                jobs.append(JobCreate(
                    link=job_url,
                    status="Open"
                ))
                
                time.sleep(random.uniform(*self.delay_between_requests))
                
            return jobs
        except Exception as e:
            logger.error(f"Error getting jobs from page: {str(e)}")
            return []

    def get_job_details(self, page: Page, url: str) -> JobDetail:
        try:
            page.goto(url, wait_until='networkidle')
            
            job_title = page.locator('h1.text-it-black').text_content()
            company_name = page.locator('div.employer-name').text_content()
            job_description = page.locator('.job-content').text_content()
            
            rows = page.query_selector_all('.row.border-bottom-dashed')
            company_info = {}
            
            for row in rows:
                text = row.inner_text()
                parts = text.split('\n')
                if len(parts) == 2:
                    company_info[parts[0]] = parts[1]
            
            return JobDetail(
                link=url,
                job_title=job_title,
                job_description=job_description,
                company_name=company_name,
                company_type=company_info.get("Company type"),
                company_industry=company_info.get("Company industry"),
                company_size=company_info.get("Company size"),
                company_country=company_info.get("Country"),
                company_working_day=company_info.get("Working days"),
                status="Open",
            )
        except Exception as e:
            logger.error(f"Error getting job details for {url}: {str(e)}")
            return JobDetail(
                link=url,
                status="Close"
            )