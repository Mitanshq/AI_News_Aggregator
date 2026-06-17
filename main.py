from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import Base, engine
from routers import auth, articles
from services.scheduler import PlatformScheduler
from routers import auth, articles, users, dashboard

# Global scheduler instance
scheduler = PlatformScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    
    # Auto-create tables (In production, use Alembic for migrations instead)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    print("Starting Autonomous Background Scheduler...")
    scheduler.start()
    
    yield # Application is running
    
    # Shutdown Sequence
    print("Shutting down scheduler and database connections...")
    scheduler.stop()
    await engine.dispose()

# Initialize FastAPI Application
app = FastAPI(
    title="AI News Platform",
    description="Autonomous Multi-Agent AI news aggregation and analysis system.",
    version="1.0.0",
    lifespan=lifespan
)

# Register Routers
app.include_router(auth.router)
app.include_router(articles.router)
app.include_router(users.router)
app.include_router(dashboard.router)

@app.get("/health", tags=["System"])
async def health_check():
    """Simple health probe for Docker/Render deployment."""
    return {"status": "operational", "agents": "online"}
