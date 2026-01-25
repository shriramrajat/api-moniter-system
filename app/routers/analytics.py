from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.database import get_db
from app.models import APILog
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/logs", description="Retrieve raw logs with filtering")
async def get_logs(
    status_code: Optional[int] = None,
    endpoint: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    min_latency: Optional[float] = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    query = select(APILog).order_by(APILog.timestamp.desc())

    if status_code:
        query = query.where(APILog.status_code == status_code)
    if endpoint:
        query = query.where(APILog.endpoint == endpoint)
    if start_time:
        query = query.where(APILog.timestamp >= start_time)
    if end_time:
        query = query.where(APILog.timestamp <= end_time)
    if min_latency:
        query = query.where(APILog.latency_ms >= min_latency)
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/summary/errors", description="Get top failing endpoints")
async def get_error_summary(db: AsyncSession = Depends(get_db)):
    """
    Returns endpoints grouped by error count (status >= 400).
    """
    # Select endpoint, count(*) from logs where status >= 400 group by endpoint order by count desc
    query = (
        select(
            APILog.endpoint,
            func.count(APILog.id).label("error_count")
        )
        .where(APILog.status_code >= 400)
        .group_by(APILog.endpoint)
        .order_by(desc("error_count"))
    )
    
    result = await db.execute(query)
    rows = result.all()
    
    return [
        {"endpoint": row.endpoint, "error_count": row.error_count}
        for row in rows
    ]

@router.get("/summary/latency", description="Get latency stats per endpoint")
async def get_latency_summary(db: AsyncSession = Depends(get_db)):
    """
    Returns average and max latency per endpoint.
    """
    query = (
        select(
            APILog.endpoint,
            func.avg(APILog.latency_ms).label("avg_latency"),
            func.max(APILog.latency_ms).label("max_latency"),
            func.count(APILog.id).label("request_count")
        )
        .group_by(APILog.endpoint)
        .order_by(desc("avg_latency"))
    )
    
    result = await db.execute(query)
    rows = result.all()
    
    return [
        {
            "endpoint": row.endpoint, 
            "avg_latency": round(row.avg_latency, 2), 
            "max_latency": round(row.max_latency, 2),
            "request_count": row.request_count
        }
        for row in rows
    ]
