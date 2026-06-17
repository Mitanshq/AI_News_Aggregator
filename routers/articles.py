from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Any
from database import get_db
from models import Article , ArticleSummary
from services.gemini import gemini_client

router = APIRouter(prefix="/articles", tags=["Intelligence Repository"])

@router.get("/latest")
async def get_latest_articles(limit: int = 10, db: AsyncSession = Depends(get_db)) -> List[dict]:
    """Retrieves the latest processed articles with their AI summaries attached."""
    query = (
        select(Article)
        .options(selectinload(Article.summary), selectinload(Article.category))
        .order_by(Article.publication_date.desc())
        .limit(limit)
    )
    result = await db.execute(query)
    articles = result.scalars().all()
    
    # Format response mapping
    return [{
        "id": a.id,
        "title": a.title,
        "source": a.source,
        "category": a.category.category if a.category else "Uncategorized",
        "importance_score": a.summary.importance_score if a.summary else 0,
        "executive_summary": a.summary.executive_summary if a.summary else "",
        "url": a.url
    } for a in articles]
