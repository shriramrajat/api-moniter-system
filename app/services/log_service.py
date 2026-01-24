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
        # No need to refresh unless we need the ID immediately, 
        # which we don't for fire-and-forget logging.
