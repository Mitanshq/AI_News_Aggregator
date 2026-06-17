from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import User
from routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["User Preferences"])


