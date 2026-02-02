import time
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.rate = requests_per_minute
        self.buckets = {}  # Dictionary to store IP -> (tokens, last_updated)

    def is_allowed(self, client_ip: str) -> bool:
        current_time = time.time()
        
        # Initialize bucket for new IP
        if client_ip not in self.buckets:
            self.buckets[client_ip] = {
                "tokens": self.rate,
                "last_updated": current_time
            }
        
        bucket = self.buckets[client_ip]
        
        # 1. Refill tokens based on time passed
        time_passed = current_time - bucket["last_updated"]
        refill_amount = time_passed * (self.rate / 60)
        bucket["tokens"] = min(self.rate, bucket["tokens"] + refill_amount)
        bucket["last_updated"] = current_time
        
        # 2. Check consumption
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        else:
            return False

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.limiter = RateLimiter(requests_per_minute)

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Skip rate limiting for static files
        if request.url.path.startswith("/static"):
             return await call_next(request)

        # Check limit
        if not self.limiter.is_allowed(client_ip):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Too Many Requests - Rate Limit Exceeded"}
            )
            
        return await call_next(request)