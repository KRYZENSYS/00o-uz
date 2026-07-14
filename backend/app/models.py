"""Database models"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, BigInteger, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import JSONB
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    USER = "user"; ADMIN = "admin"; MODERATOR = "moderator"; INVESTOR = "investor"; MENTOR = "mentor"


class StartupStage(str, enum.Enum):
    IDEA = "idea"; MVP = "mvp"; SEED = "seed"; SERIES_A = "series_a"; SERIES_B = "series_b"; GROWTH = "growth"


class StartupCategory(str, enum.Enum):
    FINTECH = "fintech"; EDTECH = "edtech"; HEALTHTECH = "healthtech"; ECOMMERCE = "ecommerce"
    SAAS = "saas"; AI = "ai"; LOGISTICS = "logistics"; AGTECH = "agtech"; MARKETPLACE = "marketplace"; OTHER = "other"


class JobType(str, enum.Enum):
    FULL_TIME = "full_time"; PART_TIME = "part_time"; CONTRACT = "contract"; FREELANCE = "freelance"; INTERNSHIP = "internship"


class NotificationType(str, enum.Enum):
    LIKE = "like"; COMMENT = "comment"; FOLLOW = "follow"; MATCH = "match"
    MESSAGE = "message"; PAYMENT = "payment"; PREMIUM = "premium"; SYSTEM = "system"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255))
    avatar_url = Column(String(500))
    bio = Column(Text)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    premium_expires = Column(DateTime)
    tokens = Column(Integer, default=0)
    telegram_id = Column(BigInteger, unique=True)
    google_id = Column(String(255), unique=True)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(32))
    reset_token = Column(String(255))
    reset_token_expires = Column(DateTime)
    ban_reason = Column(String(500))
    last_login = Column(DateTime)
    push_enabled = Column(Boolean, default=True)
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    startups = relationship("Startup", back_populates="owner", cascade="all, delete-orphan")
    services = relationship("FreelancerService", back_populates="user", cascade="all, delete-orphan")


class Startup(Base):
    __tablename__ = "startups"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    tagline = Column(String(500))
    description = Column(Text)
    logo = Column(String(500))
    cover = Column(String(500))
    website = Column(String(500))
    category = Column(SQLEnum(StartupCategory), nullable=False)
    stage = Column(SQLEnum(StartupStage), nullable=False)
    location = Column(String(255))
    team_size = Column(Integer, default=1)
    funding_raised = Column(Float, default=0)
    funding_goal = Column(Float, default=0)
    monthly_revenue = Column(Float, default=0)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="startups")


class FreelancerService(Base):
    __tablename__ = "freelancer_services"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    price_basic = Column(Float, nullable=False)
    price_standard = Column(Float)
    price_premium = Column(Float)
    delivery_days = Column(Integer, default=7)
    images = Column(JSONB, default=list)
    tags = Column(JSONB, default=list)
    rating = Column(Float, default=0)
    orders_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="services")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    category = Column(String(100), nullable=False)
    job_type = Column(SQLEnum(JobType), nullable=False)
    location = Column(String(255))
    is_remote = Column(Boolean, default=False)
    salary_min = Column(Float)
    salary_max = Column(Float)
    currency = Column(String(10), default="UZS")
    experience_years = Column(Integer, default=0)
    skills = Column(JSONB, default=list)
    applicants_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(SQLEnum(NotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSONB, default=dict)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class AIRequest(Base):
    __tablename__ = "ai_requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tool = Column(String(100), nullable=False)
    input = Column(Text, nullable=False)
    output = Column(Text)
    tokens_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="UZS")
    method = Column(String(50))
    status = Column(String(20), default="pending")
    description = Column(String(500))
    tx_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_type = Column(String(50), nullable=False)
    target_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (Index("idx_likes_user", "user_id"), Index("idx_likes_target", "target_type", "target_id"))


class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    referred_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    reward_given = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True)
    event = Column(String(100), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    data = Column(JSONB, default=dict)
    ip = Column(String(45))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
