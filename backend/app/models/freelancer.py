"""Freelancer service & job models"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class ServiceCategory(str, enum.Enum):
    WEB_DEVELOPMENT = "web_development"
    MOBILE_DEVELOPMENT = "mobile_development"
    DESIGN = "design"
    WRITING = "writing"
    MARKETING = "marketing"
    VIDEO = "video"
    AI = "ai"
    DATA = "data"
    DEVOPS = "devops"
    OTHER = "other"


class PackageType(str, enum.Enum):
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"


class FreelancerService(Base):
    __tablename__ = "freelancer_services"
    id = Column(Integer, primary_key=True, index=True)
    freelancer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(Text, nullable=False)
    category = Column(Enum(ServiceCategory), default=ServiceCategory.OTHER, index=True)
    subcategory = Column(String, nullable=True)
    cover_image = Column(String, nullable=True)
    gallery = Column(JSON, default=[])
    tags = Column(JSON, default=[])
    basic_price = Column(Float, default=0.0)
    standard_price = Column(Float, default=0.0)
    premium_price = Column(Float, default=0.0)
    basic_delivery_days = Column(Integer, default=7)
    standard_delivery_days = Column(Integer, default=14)
    premium_delivery_days = Column(Integer, default=30)
    basic_revisions = Column(Integer, default=1)
    standard_revisions = Column(Integer, default=3)
    premium_revisions = Column(Integer, default=999)
    basic_description = Column(Text, nullable=True)
    standard_description = Column(Text, nullable=True)
    premium_description = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    orders_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    favorites_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class JobType(str, enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"


class WorkMode(str, enum.Enum):
    REMOTE = "remote"
    OFFICE = "office"
    HYBRID = "hybrid"


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    employer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(Text, nullable=False)
    company_name = Column(String, nullable=True)
    company_logo = Column(String, nullable=True)
    category = Column(String, nullable=True)
    job_type = Column(Enum(JobType), default=JobType.FULL_TIME, index=True)
    work_mode = Column(Enum(WorkMode), default=WorkMode.REMOTE, index=True)
    location = Column(String, nullable=True)
    salary_min = Column(Float, default=0.0)
    salary_max = Column(Float, default=0.0)
    salary_currency = Column(String, default="UZS")
    experience_years = Column(Integer, default=0)
    skills = Column(JSON, default=[])
    requirements = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    applicants_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("freelancer_services.id"), nullable=False, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    freelancer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    package_type = Column(Enum(PackageType), default=PackageType.BASIC)
    price = Column(Float, default=0.0)
    status = Column(String, default="pending", index=True)
    requirements = Column(Text, nullable=True)
    delivery_days = Column(Integer, default=7)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
