import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Article, ArticleSummary
from agents.summarizer import SummarizerAgent
from services.gemini import gemini_client
import json, asyncio
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class ProcessingPipelineEngine:
    def __init__(self):
        self.summarizer = SummarizerAgent()
    
    async def ingest_and_process_article(self, db: AsyncSession, raw_data: dict) -> bool:
        try:
            existing_query = await db.execute(select(Article).where(Article.url == raw_data["url"]))
            if existing_query.scalar_one_or_none():
                return False
            
            article = Article(
                title=raw_data["title"],
                author=raw_data["author"],
                publication_date=raw_data["publication_date"],
                source=raw_data["source"],
                url=raw_data["url"],
                raw_content=raw_data["raw_content"],
                cleaned_content=raw_data["cleaned_content"],
                content_hash=raw_data["content_hash"],
                created_at=datetime.now(timezone.utc)
            )
            
            db.add(article)
            await db.flush()
            
            summary = await self.summarizer.process(
                article.cleaned_content
            )
            summary_record = ArticleSummary(
                article_id=article.id,
                executive_summary=summary.executive_summary,
                technical_impact=summary.technical_impact,
                business_impact=summary.business_impact,
                key_points=json.dumps(summary.key_points),
                
                importance_score=50,
                importance_reasoning="Default score",
                processed_at=datetime.now(timezone.utc)
            )
            db.add(summary_record)
            await db.flush()
        
            return True

        except Exception as e:
            logger.error(f"Pipeline execution stalled for article {raw_data.get('url')}: {str(e)}")
            await db.rollback()
            return False