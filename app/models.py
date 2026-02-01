from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from app.database import Base
from datetime import datetime

class APILog(Base):
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    method = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    latency_ms = Column(Float, nullable=False)
    error_message = Column(String, nullable=True)
    user_agent = Column(String(500), nullable=True)  

    # Indexes as per requirements
    __table_args__ = (
        Index("idx_timestamp", "timestamp"),
        Index("idx_status_code", "status_code"),
        Index("idx_endpoint", "endpoint"),
        Index("idx_timestamp_status", "timestamp", "status_code"),
    )

class LogSummary(Base):
    __tablename__ = "api_log_summaries"

    id = Column(Integer, primary_key=True, index=True)
    window_start = Column(DateTime, nullable=False)
    window_end = Column(DateTime, nullable=False)
    endpoint = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    request_count = Column(Integer, nullable=False)
    avg_latency = Column(Float, nullable=False)
    error_count = Column(Integer, nullable=False)
