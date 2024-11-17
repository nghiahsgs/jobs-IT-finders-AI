import time
import random

from src.crawlers.models.job import JobDetail
from src.crawlers.platforms.itviec_crawler import ITViecCrawler
from src.database.operations import DatabaseManager
from src.utils.browser import create_browser
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DetailCrawler:
    def __init__(self):
        self.crawler = ITViecCrawler()
        self.db = DatabaseManager()
        
    def process_single_job(self, job):
        """Process a single job with its own browser instance"""
        playwright, browser = create_browser(True)
        try:
            page = browser.new_page()
            job_details:JobDetail = self.crawler.get_job_details(page, job.link)
            if self.db.update_job(job.link, job_details):
                logger.info(f"Updated job details: {job.link}")
        except Exception as e:
            logger.error(f"Error updating job {job.link}: {str(e)}")
        finally:
            browser.close()
            playwright.stop()
            time.sleep(random.uniform(1, 3))
        
    def crawl(self):
        logger.info("Starting detail crawling process")
        jobs = self.db.get_jobs_for_update()
        logger.info(f"Found {len(jobs)} jobs to update")
        
        for job in jobs:
            self.process_single_job(job)