from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTask
from starlette.responses import Response, JSONResponse
import time
from datetime import datetime
from app.services.log_service import create_log_entry
import traceback

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. START CLOCK
        # We need high-precision timing to measure latency accurately.
        start_time = time.time()
        # We needs the actual timestamp for the database record.
        start_datetime = datetime.utcnow()
        
        method = request.method
        endpoint = request.url.path
        
        # Optional: Skip health checks to avoid polluting logs
        if endpoint == "/health":
             return await call_next(request)

        error_message = None
        status_code = 500 # Assume failure unless proven otherwise

        try:
            # 2. PROCESS REQUEST
            # This passes the ball to the actual application (routers/endpoints).
            response = await call_next(request)
            
            # If we get here, the app didn't crash! Capture the real status code.
            status_code = response.status_code

        except Exception as e:
            # 3. CATCH EXCEPTIONS
            # If the app crashs (unhandled exception), we catch it here so the logging doesn't fail.
            print(f"Middleware caught an error: {e}")
            error_message = str(e) # e.g., "Division by zero"
            status_code = 500      # Internal Server Error
            
            # We must still return a valid HTTP response to the user.
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error - Cached by Middleware"}
            )
            # Optional: Print stack trace to console for local debugging
            traceback.print_exc()

        # 4. STOP CLOCK
        duration = time.time() - start_time
        latency_ms = duration * 1000 # Convert seconds to milliseconds

        # 5. ASYNC DISPATCH (FIRE AND FORGET)
        # We attach the DB write as a "background task". 
        # FastAPI will send the response to the user FIRST, then run this function.
        # This ensures logging never slows down the user's response time.
        
        log_task = BackgroundTask(
            create_log_entry,
            timestamp=start_datetime,
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            latency_ms=latency_ms,
            error_message=error_message
        )
        
        # If the response already has a background task, we must chain them.
        if response.background:
            previous_task = response.background
            async def composite_task():
                await previous_task()
                await log_task()
            response.background = BackgroundTask(composite_task)
        else:
            response.background = log_task
            
        return response
