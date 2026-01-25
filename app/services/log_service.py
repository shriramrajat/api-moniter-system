from sqlalchemy.ext.asyncio import AsyncSession
from app.models import APILog
from app.database import AsyncSessionLocal
from datetime import datetime

async def create_log_entry(
    timestamp: datetime,
    method: str,
    endpoint: str,
    status_code: int,
    latency_ms: float,
    error_message: str = None
):
    """
    Writes a log entry to the database asynchronously.
    
    CRITICAL:
    This function creates its own isolated database session (`AsyncSessionLocal`).
    It does NOT use the dependency injection session from the main request, 
    because that session might be closed by the time this background task runs.
    """
    
    # 1. Enforce UTC (Data Integrity)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=None) # Ensure naive UTC for Postgres default

    # 2. Safety Truncation (Anti-Flooding)
    # If an error trace is huge, we chop it. monitoring shouldn't crash the DB.
    if error_message and len(error_message) > 1000:
        error_message = error_message[:1000] + "...[TRUNCATED]"

    async with AsyncSessionLocal() as session:
        log_entry = APILog(
            timestamp=timestamp, # Now strictly managed
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            latency_ms=latency_ms,
            error_message=error_message
        )
        session.add(log_entry)
        await session.commit()
        # No need to refresh unless we need the ID immediately, 
        # which we don't for fire-and-forget logging.
