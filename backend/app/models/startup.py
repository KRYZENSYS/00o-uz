"""Startup model"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class StartupStage(str, enum.Enum):
    IDEA = "idea"
    MVP = "mvp"
    EARLY = "early"
    GROWTH = "growth"
    SCALE = "scale"


class StartupCategory(str, enum.Enum):
    FINTECH = "fintech"
    EDTECH = "edtech"
    HEALTHTECH = "healthtech"
    AGRITECH = "agritech"
    ECOMMERCE = "ecommerce"
    SAAS = "saas"
    AI = "ai"
    BLOCKCHAIN = "blockchain"
    LOGISTICS = "logistics"
    OTHER = "other"


class Startup(Base):
    __tablename__ = "startups"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True)
    tagline = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    category = Column(Enum(StartupCategory), default=StartupCategory.OTHER, index=True)
    stage = Column(Enum(StartupStage), default=StartupStage.IDEA, index=True)
    logo = Column(String, nullable=True)
    banner = Column(String, nullable=True)
    website = Column(String, nullable=True)
    github = Column(String, nullable=True)
    pitch_deck_url = Column(String, nullable=True)
    business_plan_url = Column(String, nullable=True)
    funding_goal = Column(Float, default=0.0)
    funding_raised = Column(Float, default=0.0)
    equity_offered = Column(Float, default=0.0)
    min_investment = Column(Float, default=0.0)
    max_investment = Column(Float, default=0.0)
    team_size = Column(Integer, default=1)
    location = Column(String, nullable=True)
    founded_year = Column(Integer, nullable=True)
    is_verified = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    followers_count = Column(Integer, default=0)
    tags = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
