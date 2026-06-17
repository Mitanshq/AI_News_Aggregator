from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# ==========================================
# API Request & Response Schemas
# ==========================================

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}



# ==========================================
# AI Agent Structured Output Schemas
# ==========================================

class AgentSummaryOutput(BaseModel):
    executive_summary: str = Field(description="A concise 2-3 sentence executive summary.")
    technical_impact: str = Field(description="The technical implications for engineers and researchers.")
    business_impact: str = Field(description="The business and market implications of the news.")
    key_points: list[str] = Field(description="Top 3 to 5 bullet points extracted from the article.")



