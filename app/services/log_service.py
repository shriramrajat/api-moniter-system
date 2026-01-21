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
    This creates its own session to ensure it doesn't interfere with the main request scope
    if called in background.
    """
    async with AsyncSessionLocal() as session:
        log_entry = APILog(
            timestamp=timestamp,
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            latency_ms=latency_ms,
            error_message=error_message
        )
        session.add(log_entry)
        await session.commit()
