import time
import random
from typing import List

from src.crawlers.models.job import JobCreate
from src.crawlers.platforms.itviec_crawler import ITViecCrawler
from src.database.operations import DatabaseManager
from src.utils.logger import get_logger
from src.utils.browser import create_browser

logger = get_logger(__name__)

class JobCrawler:
    def __init__(self):
        self.crawler = ITViecCrawler()
        self.db = DatabaseManager()

    def get_max_pages(self) -> int:
        """Get max pages with a separate browser instance"""
        playwright, browser = create_browser(True)
        try:
            page = browser.new_page()
            page.goto(ITViecCrawler.BASE_URL, wait_until='networkidle')
            return self.crawler.get_max_pages(page)
        except Exception as e:
            logger.error(f"Error getting max pages: {str(e)}")
            return 1
        finally:
            browser.close()
            playwright.stop()


    def process_single_page(self, page_num: int, max_pages: int):
        """Process a single page with its own browser instance"""
        playwright, browser = create_browser(True)
        try:
            page = browser.new_page()
            page.goto(f"{ITViecCrawler.BASE_URL}?page={page_num}", wait_until='networkidle')
            logger.info(f"Crawling page {page_num}/{max_pages}")
            
            jobs:List[JobCreate] = self.crawler.get_jobs_from_page(page)
            for job in jobs:
                if self.db.add_job(job):
                    logger.info(f"Added new job: {job.link}")  # Using Pydantic model attribute
                
        except Exception as e:
            logger.error(f"Error processing page {page_num}: {str(e)}")
        finally:
            browser.close()
            playwright.stop()
            time.sleep(random.uniform(3, 7))

    def crawl(self):
        logger.info("Starting job crawling process")
        max_pages = self.get_max_pages()
        
        for page_num in range(1, max_pages + 1):
            self.process_single_page(page_num, max_pages)