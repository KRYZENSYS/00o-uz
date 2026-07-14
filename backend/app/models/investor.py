"""Investor & AI models"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, JSON, Boolean
from app.core.database import Base


class Investor(Base):
    __tablename__ = "investors"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    firm_name = Column(String, nullable=True)
    investment_range_min = Column(Float, default=0.0)
    investment_range_max = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    interests = Column(JSON, default=[])
    stages = Column(JSON, default=[])
    geography = Column(JSON, default=[])
    portfolio = Column(JSON, default=[])
    total_invested = Column(Float, default=0.0)
    investments_count = Column(Integer, default=0)
    bio = Column(Text, nullable=True)
    website = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class InvestmentOffer(Base):
    __tablename__ = "investment_offers"
    id = Column(Integer, primary_key=True, index=True)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=False, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    equity = Column(Float, default=0.0)
    valuation = Column(Float, default=0.0)
    message = Column(Text, nullable=True)
    status = Column(String, default="pending", index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    responded_at = Column(DateTime, nullable=True)


class TeamRequest(Base):
    __tablename__ = "team_requests"
    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String, nullable=False)
    message = Column(Text, nullable=True)
    status = Column(String, default="pending", index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class AIConversation(Base):
    __tablename__ = "ai_conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tool = Column(String, nullable=False, index=True)
    title = Column(String, nullable=True)
    model = Column(String, default="llama-3.3-70b-versatile")
    language = Column(String, default="uz")
    total_tokens = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AIMessage(Base):
    __tablename__ = "ai_messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("ai_conversations.id"), nullable=False, index=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tokens = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class AILog(Base):
    __tablename__ = "ai_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    tool = Column(String, nullable=False, index=True)
    model = Column(String, nullable=False)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    duration_ms = Column(Integer, default=0)
    status = Column(String, default="success")
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
