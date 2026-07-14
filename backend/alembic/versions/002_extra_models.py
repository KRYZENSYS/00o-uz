"""Alembic migration - extended models"""
"""add extended models

Revision ID: 002
Revises: 001
Create Date: 2026-07-14
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID
import enum


revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Chat model
    op.create_table('chats',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('is_group', sa.Boolean, default=False),
        sa.Column('name', sa.String(255)),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('last_message_id', sa.Integer),
        sa.Column('last_message_at', sa.DateTime),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    op.create_index('idx_chats_last_msg', 'chats', ['last_message_at'])
    
    op.create_table('chat_participants',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('chat_id', sa.Integer, sa.ForeignKey('chats.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('joined_at', sa.DateTime, server_default=sa.func.now()),
        sa.UniqueConstraint('chat_id', 'user_id', name='uq_chat_user')
    )
    op.create_index('idx_chat_user', 'chat_participants', ['user_id'])
    
    # Messages already exists from 001, add chat_id if needed
    # Posts
    op.create_table('posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('images', JSONB, default=list),
        sa.Column('tags', JSONB, default=list),
        sa.Column('visibility', sa.String(20), default='public'),
        sa.Column('likes_count', sa.Integer, default=0),
        sa.Column('comments_count', sa.Integer, default=0),
        sa.Column('shares_count', sa.Integer, default=0),
        sa.Column('views_count', sa.Integer, default=0),
        sa.Column('is_pinned', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    op.create_index('idx_posts_user', 'posts', ['user_id'])
    op.create_index('idx_posts_created', 'posts', ['created_at'])
    
    op.create_table('comments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('parent_id', sa.Integer, sa.ForeignKey('comments.id')),
        sa.Column('likes_count', sa.Integer, default=0),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    op.create_index('idx_comments_post', 'comments', ['post_id'])
    
    # Follow
    op.create_table('follows',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('follower_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('following_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.UniqueConstraint('follower_id', 'following_id', name='uq_follow')
    )
    op.create_index('idx_follow_follower', 'follows', ['follower_id'])
    op.create_index('idx_follow_following', 'follows', ['following_id'])
    
    # Team
    op.create_table('teams',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('startup_id', sa.Integer, sa.ForeignKey('startups.id')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('looking_for', JSONB, default=list),
        sa.Column('skills_needed', JSONB, default=list),
        sa.Column('members_count', sa.Integer, default=1),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_featured', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    
    op.create_table('team_members',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('team_id', sa.Integer, sa.ForeignKey('teams.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('role', sa.Enum('owner', 'cofounder', 'developer', 'designer', 'marketer', 'mentor', name='team_role'), default='developer'),
        sa.Column('equity', sa.Float, default=0),
        sa.Column('joined_at', sa.DateTime, server_default=sa.func.now()),
        sa.UniqueConstraint('team_id', 'user_id', name='uq_team_member')
    )
    
    op.create_table('applications',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('team_id', sa.Integer, sa.ForeignKey('teams.id'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('role', sa.String(50), default='developer'),
        sa.Column('message', sa.Text),
        sa.Column('status', sa.Enum('pending', 'accepted', 'rejected', name='app_status'), default='pending'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    
    # Investors
    op.create_table('investors',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.Enum('angel', 'vc', 'fund', 'accelerator', 'syndicate', name='investor_type'), nullable=False),
        sa.Column('bio', sa.Text),
        sa.Column('min_investment', sa.Float, default=0),
        sa.Column('max_investment', sa.Float, default=0),
        sa.Column('currency', sa.String(10), default='USD'),
        sa.Column('industries', JSONB, default=list),
        sa.Column('stages', JSONB, default=list),
        sa.Column('location', sa.String(255)),
        sa.Column('website', sa.String(500)),
        sa.Column('portfolio_count', sa.Integer, default=0),
        sa.Column('total_invested', sa.Float, default=0),
        sa.Column('is_verified', sa.Boolean, default=False),
        sa.Column('is_featured', sa.Boolean, default=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    
    op.create_table('deals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('startup_id', sa.Integer, sa.ForeignKey('startups.id'), nullable=False),
        sa.Column('investor_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('equity', sa.Float, nullable=False),
        sa.Column('valuation', sa.Float, default=0),
        sa.Column('message', sa.Text),
        sa.Column('status', sa.Enum('pending', 'accepted', 'rejected', 'completed', name='deal_status'), default='pending'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    
    # Courses
    op.create_table('courses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('instructor_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('instructor_name', sa.String(255)),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('category', sa.String(100), nullable=False, index=True),
        sa.Column('level', sa.Enum('beginner', 'intermediate', 'advanced', name='course_level'), default='beginner'),
        sa.Column('price', sa.Float, default=0),
        sa.Column('cover_image', sa.String(500)),
        sa.Column('tags', JSONB, default=list),
        sa.Column('students_count', sa.Integer, default=0),
        sa.Column('rating', sa.Float, default=0),
        sa.Column('lessons_count', sa.Integer, default=0),
        sa.Column('duration_hours', sa.Float, default=0),
        sa.Column('is_published', sa.Boolean, default=False),
        sa.Column('is_featured', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    
    op.create_table('lessons',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text),
        sa.Column('video_url', sa.String(500)),
        sa.Column('duration', sa.Integer, default=0),
        sa.Column('order', sa.Integer, default=0),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    
    op.create_table('enrollments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('courses.id'), nullable=False),
        sa.Column('progress', sa.Integer, default=0),
        sa.Column('completed_lessons', JSONB, default=list),
        sa.Column('enrolled_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime),
        sa.UniqueConstraint('user_id', 'course_id', name='uq_enrollment')
    )
    
    # Add user extra fields
    op.add_column('users', sa.Column('company', sa.String(255)))
    op.add_column('users', sa.Column('position', sa.String(255)))
    op.add_column('users', sa.Column('website', sa.String(500)))
    op.add_column('users', sa.Column('github', sa.String(255)))
    op.add_column('users', sa.Column('twitter', sa.String(255)))
    op.add_column('users', sa.Column('linkedin', sa.String(255)))


def downgrade():
    op.drop_table('enrollments')
    op.drop_table('lessons')
    op.drop_table('courses')
    op.drop_table('deals')
    op.drop_table('investors')
    op.drop_table('applications')
    op.drop_table('team_members')
    op.drop_table('teams')
    op.drop_table('follows')
    op.drop_table('comments')
    op.drop_table('posts')
    op.drop_table('chat_participants')
    op.drop_table('chats')
    op.drop_column('users', 'linkedin')
    op.drop_column('users', 'twitter')
    op.drop_column('users', 'github')
    op.drop_column('users', 'website')
    op.drop_column('users', 'position')
    op.drop_column('users', 'company')
