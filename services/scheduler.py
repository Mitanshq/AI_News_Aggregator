import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from services.scraper import NewsScraper
from services.pipeline import ProcessingPipelineEngine
from database import AsyncSessionLocal
from sqlalchemy import select

from models import (
    User,
    Article,
    ArticleSummary
)

from services.email_service import email_service

logger = logging.getLogger(__name__)

class PlatformScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.pipeline = ProcessingPipelineEngine()

    async def run_hourly_collection(self):
        """Task 1: Hourly news scraping and multi-agent processing."""
        logger.info("Initiating hourly collection cycle.")
        scraper = NewsScraper()
        raw_articles = await scraper.run_collection_cycle()
        
        processed_count = 0
        async with AsyncSessionLocal() as db:
            for raw_data in raw_articles:
                success = await self.pipeline.ingest_and_process_article(db, raw_data)
                if success:
                    processed_count += 1
                    await db.commit() # Commit individually to save progress
                    
        await scraper.close()
        logger.info(f"Hourly cycle complete. Successfully processed {processed_count} new articles.")

    async def run_daily_newsletter_generation(self):
        logger.info("Initiating daily executive newsletter generation.")

        async with AsyncSessionLocal() as db:

            # Get active users
            users = await db.execute(
                select(User).where(User.is_active == True)
            )

            users = users.scalars().all()

            # Get today's articles with summaries
            articles = await db.execute(
                select(Article, ArticleSummary)
                .join(
                    ArticleSummary,
                    Article.id == ArticleSummary.article_id
                )
                .order_by(Article.publication_date.desc())
                .limit(20)
            )

            articles = articles.all()

            if not articles:
                logger.info("No articles available for newsletter.")
                return

            # Build newsletter HTML
            html_content = """
            <html>
            <body>
            <h1>Daily AI News Digest</h1>
            """

            for article, summary in articles:
                html_content += f"""
                <hr>
                <h2>{article.title}</h2>

                <p>
                <strong>Executive Summary:</strong><br>
                {summary.executive_summary}
                </p>

                <p>
                <strong>Technical Impact:</strong><br>
                {summary.technical_impact}
                </p>

                <p>
                <strong>Business Impact:</strong><br>
                {summary.business_impact}
                </p>

                <a href="{article.url}">
                    Read Full Article
                </a>
                """

            html_content += """
            </body>
            </html>
            """

            # Send to all users
            for user in users:
                try:
                    await email_service.send_email(
                        to_email='mitanshcr7@gmail.com',
                        subject="Daily AI News Digest",
                        html_content=html_content
                    )

                    logger.info(
                        f"Newsletter sent to {user.email}"
                    )

                except Exception as e:
                    logger.error(
                        f"Failed sending newsletter to {user.email}: {e}"
                    )

    def start(self):
        # Schedule Scraping Every Hour
        self.scheduler.add_job(
            self.run_hourly_collection,
            CronTrigger(minute=47) # Runs at minute 0 of every hour
        )
        
        # Schedule Newsletter Dispatch Daily at 7:00 AM UTC
        self.scheduler.add_job(
            self.run_daily_newsletter_generation,
            CronTrigger(hour=13, minute=48)
        )
        
        self.scheduler.start()
        logger.info("Autonomous AI Scheduler Started.")

    def stop(self):
        self.scheduler.shutdown()