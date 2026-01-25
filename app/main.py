from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.middleware import LoggingMiddleware
from app.database import engine, Base
from app.routers import analytics
import random
import time
import os

app = FastAPI(title="API Log & Monitoring System")

# Add Middleware
app.add_middleware(LoggingMiddleware)

# Include Routers
app.include_router(analytics.router)

# Startup Event to Create Tables (For Dev Simplicity)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    with open(os.path.join("app", "static", "dashboard.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/")
async def root():
    return {"message": "System Operational"}

@app.get("/users")
async def get_users():
    # Simulate work
    time.sleep(random.uniform(0.1, 0.3)) # Note: time.sleep blocks, but for demo okay.
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@app.get("/error")
async def trigger_error():
    # Simulate failure
    raise ValueError("Something went wrong!")

@app.get("/slow")
async def slow_endpoint():
    # Simulate high latency
    import asyncio
    await asyncio.sleep(1.5)
    return {"message": "That was slow"}
