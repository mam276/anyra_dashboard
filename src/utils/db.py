from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

Base = declarative_base()
engine = create_engine("sqlite:///anyra.db")
SessionLocal = sessionmaker(bind=engine)

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

Base.metadata.create_all(engine)