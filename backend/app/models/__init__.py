"""User model"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class UserRole(str, enum.Enum):
    USER = "user"
    FREELANCER = "freelancer"
    STARTUP_OWNER = "startup_owner"
    INVESTOR = "investor"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    BANNED = "banned"
    PENDING = "pending"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    phone = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    cover = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    website = Column(String, nullable=True)
    github = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    telegram_username = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER, index=True)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING, index=True)
    is_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String, nullable=True)
    language = Column(String, default="uz")
    timezone = Column(String, default="Asia/Tashkent")
    last_login_at = Column(DateTime, nullable=True)
    last_seen_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
