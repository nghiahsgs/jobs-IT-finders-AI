from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from src.crawlers.services.job_crawler import JobCrawler
from src.crawlers.services.detail_crawler import DetailCrawler
from src.utils.logger import get_logger


logger = get_logger(__name__)

def start_scheduler():
    scheduler = BlockingScheduler()
    
    ## Crawl new jobs every day at 00:00
    scheduler.add_job(
        JobCrawler().crawl,
        # trigger=CronTrigger(hour=0, minute=0),
        trigger=CronTrigger(hour='*/12'),  # Run every 12 hours
        next_run_time=datetime.now(),     # Run immediately the first time
        id='crawl_new_jobs',
        name='Crawl new jobs'
    )
    
    ## Crawl job details every 4 hours
    scheduler.add_job(
        DetailCrawler().crawl,
        trigger=CronTrigger(hour='*/12'),  # Run every 12 hours
        next_run_time=datetime.now(),     # Run immediately the first time
        id='crawl_job_details',
        name='Crawl job details'
    )
    
    logger.info('Starting scheduler...')
    scheduler.start()