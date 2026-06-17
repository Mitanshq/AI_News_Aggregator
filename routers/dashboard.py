from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.future import select
from database import get_db
from models import User, Article
from routers.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Admin Analytics"])

async def verify_admin_status(current_user: User = Depends(get_current_user)):
    """Security guard verifying administrative credentials."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Administrative privileges required."
        )
    return current_user

@router.get("/metrics", dependencies=[Depends(verify_admin_status)])
async def get_platform_analytics(db: AsyncSession = Depends(get_db)):
    """Computes high-level cross-sectional health metrics across tables."""
    # Count aggregates asynchronously
    total_users_query = await db.execute(select(func.count(User.id)))
    total_articles_query = await db.execute(select(func.count(Article.id)))


    return {
        "overview": {
            "total_subscribers": total_users_query.scalar() or 0,
            "processed_articles_volume": total_articles_query.scalar() or 0,
        },
    }