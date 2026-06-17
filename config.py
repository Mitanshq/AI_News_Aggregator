import os 
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, EmailStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    ENV: str = Field(default="production", json_schema_extra={"env": "ENV"})
    PROJECT_NAME: str = "AI News Platform"
    
    SECRET_KEY: str = Field(..., json_schema_extra={"env": "SECRET_KEY"})
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    DATABASE_URL: str = Field(..., json_schema_extra={"env": "DATABASE_URL"})
    
    GEMINI_API_KEY: str = Field(..., json_schema_extra={"env": "GEMINI_API_KEY"})
    
    MODEL_SUMMARY: str = 'gemma3:12b'
    MODEL_NEWSLETTER: str = 'gemma3:12b'
    
    SMTP_HOST: str = Field(default="smtp.gmail.com", json_schema_extra={"env": "SMTP_HOST"})
    SMTP_PORT: int = Field(default=587, json_schema_extra={"env": "SMTP_PORT"})
    SMTP_USER: str = Field(default=..., json_schema_extra={"env": "SMTP_USER"})
    SMTP_PASSWORD: str = Field(default=..., json_schema_extra={"env": "SMTP_PASSWORD"})
    EMAIL_FROM: EmailStr = Field(default="digest@platform.ai", json_schema_extra={"env": "EMAIL_FROM"})
    
settings = Settings()