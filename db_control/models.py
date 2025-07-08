# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, nullable=False)
    zebra_id = Column(String(64), nullable=False)
    campaign_name = Column(String(128), nullable=False)
    uid = Column(String(64), unique=True, nullable=False)
    target_url = Column(String(2048), nullable=False) 
    slug = Column(String(255), unique=True, nullable=True)
    access_count = Column(Integer, default=0)
    last_accessed_at = Column(DateTime, nullable=True)