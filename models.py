import datetime
from typing import List, Optional
from sqlalchemy import Table, Column, Integer, func, String, Text, DateTime, Boolean, ForeignKey, Float, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from sqlalchemy import Text


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    preferences: Mapped[Optional["UserPreference"]] = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    digests: Mapped[List["Digest"]] = relationship("Digest", back_populates="user", cascade="all, delete-orphan")
    email_logs: Mapped[List["EmailLog"]] = relationship("EmailLog", back_populates="user", cascade="all, delete-orphan")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    preferred_topics: Mapped[str] = mapped_column(Text, default="")
    preferred_companies: Mapped[str] = mapped_column(Text, default="")
    delivery_frequency: Mapped[str] = mapped_column(String(50), default="daily") # daily, weekly, paused
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="preferences")


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    author: Mapped[Optional[str]] = mapped_column(String(255))
    publication_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    source: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    url: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    cleaned_content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    # Relationships
    summary: Mapped[Optional["ArticleSummary"]] = relationship("ArticleSummary", back_populates="article", uselist=False, cascade="all, delete-orphan")


class ArticleSummary(Base):
    __tablename__ = "article_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), unique=True, nullable=False)
    executive_summary: Mapped[str] = mapped_column(Text, nullable=False)
    technical_impact: Mapped[str] = mapped_column(Text, nullable=False)
    business_impact: Mapped[str] = mapped_column(Text, nullable=False)
    key_points: Mapped[str] = mapped_column(Text, nullable=False)
    importance_score: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    importance_reasoning: Mapped[str] = mapped_column(Text, nullable=False)
    processed_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    # Relationships
    article: Mapped["Article"] = relationship("Article", back_populates="summary")




class Digest(Base):
    __tablename__ = "digests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    html_content: Mapped[str] = mapped_column(Text, nullable=False)
    generated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    sent_status: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="digests")


class EmailLog(Base):
    __tablename__ = "email_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    delivery_type: Mapped[str] = mapped_column(String(50)) # verification, digest, alert
    status: Mapped[str] = mapped_column(String(50)) # success, failed
    error_details: Mapped[Optional[str]] = mapped_column(Text)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="email_logs")

