"""
Scheduler Service - Automated Background Jobs

This service uses APScheduler to run periodic tasks without blocking the main application.
Currently schedules:
- Hourly aggregation of API logs into summary tables
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging

# Import our aggregation service
from app.services.aggregation_service import run_aggregation_job

# Setup logging
logger = logging.getLogger(__name__)

# Create a global scheduler instance
scheduler = AsyncIOScheduler()


def start_scheduler():
    """
    Start the background scheduler.
    
    This function is called once when the FastAPI app starts.
    It schedules the aggregation job to run every hour.
    """
    
    # Schedule: Run aggregate_logs() every 1 hour
    # Note: We don't run immediately on startup to avoid event loop issues
    # First run will be 1 hour after server starts
    scheduler.add_job(
        func=run_aggregation_job,            # The function to run
        trigger=IntervalTrigger(hours=1), # Run every 1 hour
        id="hourly_aggregation",          # Unique job ID
        name="Aggregate API Logs",        # Human-readable name
        replace_existing=True             # Replace if job already exists
    )
    
    # Start the scheduler
    scheduler.start()
    logger.info("✅ Scheduler started - Aggregation will run every hour")


def stop_scheduler():
    """
    Stop the scheduler gracefully.
    
    Called when the FastAPI app shuts down.
    """
    scheduler.shutdown()
    logger.info("🛑 Scheduler stopped")