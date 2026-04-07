from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, PRIMARY KEY=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    api_key = Column(String, unique=True) # For programmatic access

class MigrationJob(Base):
    __tablename__ = "migration_jobs"
    id = Column(Integer, PRIMARY KEY=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_name = Column(String)
    source_config = Column(JSON)      # IP, Port, DB Name (Encrypted)
    dest_config = Column(JSON)        # S3 Path, CSV name
    status = Column(String, default="PENDING") # RUNNING, COMPLETED, FAILED
    progress = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, PRIMARY KEY=True, index=True)
    job_id = Column(Integer, ForeignKey("migration_jobs.id"))
    level = Column(String)            # INFO, ERROR, WARNING
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)