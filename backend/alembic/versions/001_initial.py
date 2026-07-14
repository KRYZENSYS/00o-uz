"""Initial migration"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, ENUM

revision = '001'
down_revision = None


def upgrade():
    user_role = ENUM('user', 'admin', 'moderator', 'investor', 'mentor', name='userrole', create_type=True)
    startup_stage = ENUM('idea', 'mvp', 'seed', 'series_a', 'series_b', 'growth', name='startupstage', create_type=True)
    startup_category = ENUM('fintech', 'edtech', 'healthtech', 'ecommerce', 'saas', 'ai', 'logistics', 'agtech', 'marketplace', 'other', name='startupcategory', create_type=True)
    notification_type = ENUM('like', 'comment', 'follow', 'match', 'message', 'payment', 'premium', 'system', name='notificationtype', create_type=True)
    job_type = ENUM('full_time', 'part_time', 'contract', 'freelance', 'internship', name='jobtype', create_type=True)

    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('phone', sa.String(20), unique=True, nullable=True),
        sa.Column('username', sa.String(64), unique=True, index=True, nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=True),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('bio', sa.Text, nullable=True),
        sa.Column('role', user_role, default='user'),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_verified', sa.Boolean, default=False),
        sa.Column('is_premium', sa.Boolean, default=False),
        sa.Column('premium_expires', sa.DateTime, nullable=True),
        sa.Column('tokens', sa.Integer, default=0),
        sa.Column('telegram_id', sa.BigInteger, unique=True, nullable=True),
        sa.Column('google_id', sa.String(255), unique=True, nullable=True),
        sa.Column('two_factor_enabled', sa.Boolean, default=False),
        sa.Column('two_factor_secret', sa.String(32), nullable=True),
        sa.Column('reset_token', sa.String(255), nullable=True),
        sa.Column('reset_token_expires', sa.DateTime, nullable=True),
        sa.Column('ban_reason', sa.String(500), nullable=True),
        sa.Column('last_login', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_table('startups',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('slug', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('tagline', sa.String(500), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('logo', sa.String(500), nullable=True),
        sa.Column('website', sa.String(500), nullable=True),
        sa.Column('category', startup_category, nullable=False),
        sa.Column('stage', startup_stage, nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('team_size', sa.Integer, default=1),
        sa.Column('funding_raised', sa.Float, default=0),
        sa.Column('views_count', sa.Integer, default=0),
        sa.Column('likes_count', sa.Integer, default=0),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_verified', sa.Boolean, default=False),
        sa.Column('is_featured', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )

    op.create_table('freelancer_services',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('category', sa.String(100), nullable=False, index=True),
        sa.Column('price_basic', sa.Float, nullable=False),
        sa.Column('price_standard', sa.Float, nullable=True),
        sa.Column('price_premium', sa.Float, nullable=True),
        sa.Column('delivery_days', sa.Integer, default=7),
        sa.Column('images', JSONB, default=list),
        sa.Column('tags', JSONB, default=list),
        sa.Column('rating', sa.Float, default=0),
        sa.Column('orders_count', sa.Integer, default=0),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )

    op.create_table('jobs',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('company_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('job_type', job_type, nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('is_remote', sa.Boolean, default=False),
        sa.Column('salary_min', sa.Float, nullable=True),
        sa.Column('salary_max', sa.Float, nullable=True),
        sa.Column('currency', sa.String(10), default='UZS'),
        sa.Column('skills', JSONB, default=list),
        sa.Column('applicants_count', sa.Integer, default=0),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )

    op.create_table('notifications',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('type', notification_type, nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('data', JSONB, default=dict),
        sa.Column('is_read', sa.Boolean, default=False),
        sa.Column('read_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )

    op.create_table('ai_requests',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('tool', sa.String(100), nullable=False),
        sa.Column('input', sa.Text, nullable=False),
        sa.Column('output', sa.Text, nullable=True),
        sa.Column('tokens_used', sa.Integer, default=0),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )

    op.create_table('transactions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('currency', sa.String(10), default='UZS'),
        sa.Column('method', sa.String(50), nullable=True),
        sa.Column('status', sa.String(20), default='pending'),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )

    op.create_table('likes',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('target_type', sa.String(50), nullable=False),
        sa.Column('target_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )

    op.create_table('referrals',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('referrer_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('referred_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False, unique=True),
        sa.Column('reward_given', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )


def downgrade():
    op.drop_table('referrals')
    op.drop_table('likes')
    op.drop_table('transactions')
    op.drop_table('ai_requests')
    op.drop_table('notifications')
    op.drop_table('jobs')
    op.drop_table('freelancer_services')
    op.drop_table('startups')
    op.drop_table('users')
