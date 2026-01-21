from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTask
from starlette.responses import Response
import time
from datetime import datetime
from app.services.log_service import create_log_entry
import traceback

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        start_datetime = datetime.utcnow()
        
        method = request.method
        endpoint = request.url.path
        
        # Skip health check or ignored paths if necessary (optional)
        # if endpoint == "/health":
        #     return await call_next(request)

        error_message = None
        status_code = 500 # Default to 500 until proven otherwise

        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            # We caught an unhandled exception!
            error_message = str(e)
            # We must return a response to the user, typically a 500
            # For simplicity, we re-raise or return a generic 500 JSON response
            # But to capture the log, we proceed here.
            # In a real app, you might want to format the error response.
            # Here we just want to ensure we log it.
            status_code = 500
            
            # Re-creating a response object to attach background task
            from fastapi.responses import JSONResponse
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"}
            )
            print(f"Captured Exception: {traceback.format_exc()}") # Print trace for debugging

        duration = time.time() - start_time
        latency_ms = duration * 1000

        # Create the background task for logging
        task = BackgroundTask(
            create_log_entry,
            timestamp=start_datetime,
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            latency_ms=latency_ms,
            error_message=error_message
        )
        
        # Append to existing background tasks if any
        if response.background:
            previous_task = response.background
            async def composite_task():
                await previous_task()
                await task()
            response.background = BackgroundTask(composite_task)
        else:
            response.background = task
            
        return response
