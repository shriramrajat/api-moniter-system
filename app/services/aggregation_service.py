from app.database import AsyncSessionLocal
from app.models import APILog, LogSummary
from sqlalchemy import select, func, and_, case
from datetime import datetime, timedelta

async def run_aggregation_job(window_minutes=60):
    """
    Background job to aggregate raw logs into summaries.
    Currently hardcoded to aggregate the 'last hour'.
    In a real system, you'd track the 'last_aggregated_time' to avoid gaps.
    """
    print(f"[{datetime.utcnow()}] 🔄 Starting Log Aggregation Job...")
    
    async with AsyncSessionLocal() as session:
        # Define window
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=window_minutes)
        
        # 1. Fetch Aggregated Data from Raw Logs
        # GROUP BY endpoint, status_code
        query = (
            select(
                APILog.endpoint,
                APILog.status_code,
                func.count(APILog.id).label("request_count"),
                func.avg(APILog.latency_ms).label("avg_latency"),
                func.sum(
                    case((APILog.status_code >= 400, 1), else_=0)
                ).label("error_count")
            )
            .where(APILog.timestamp >= start_time)
            .group_by(APILog.endpoint, APILog.status_code)
        )
        
        result = await session.execute(query)
        aggregates = result.all()
        
        if not aggregates:
            print("   ⚠️ No logs found to aggregate.")
            return

        print(f"   ✅ Found {len(aggregates)} groupings to summarize.")

        # 2. Insert into Summary Table
        for row in aggregates:
            summary = LogSummary(
                window_start=start_time,
                window_end=end_time,
                endpoint=row.endpoint,
                status_code=row.status_code,
                request_count=row.request_count,
                avg_latency=row.avg_latency,
                error_count=row.error_count or 0 # Handle None if no errors
            )
            session.add(summary)
        
        await session.commit()
        print("   💾 Summaries saved to database.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_aggregation_job())
