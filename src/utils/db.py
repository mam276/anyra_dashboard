import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

# Base class for SQLAlchemy models
Base = declarative_base()

# Load Neon connection string from Streamlit secrets
DATABASE_URL = st.secrets["DATABASE_URL"]

# Create SQLAlchemy engine
# Neon requires SSL, already included in the URL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,     # Ensures stale connections are refreshed
    echo=False              # Set to True only for debugging
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -------------------------
#       MODELS
# -------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    subscription = Column(String, default="free")
    remember_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    action = Column(String)
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    plan = Column(String)
    active = Column(Boolean, default=True)
    trial_end_date = Column(DateTime)


# -------------------------
#   CREATE TABLES
# -------------------------

try:
    Base.metadata.create_all(engine)
    print("Neon DB connected and tables created successfully.")
except Exception as e:
    print("Error initializing database:", e)
