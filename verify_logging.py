import asyncio
import httpx
from app.database import AsyncSessionLocal
from app.models import APILog
from sqlalchemy import select

BASE_URL = "http://127.0.0.1:8000"

async def generate_traffic():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        print("1. Sending Request: GET / (Success)")
        await client.get("/")
        
        print("2. Sending Request: GET /users (Success)")
        await client.get("/users")
        
        print("3. Sending Request: GET /error (Should Fail)")
        try:
            await client.get("/error")
        except:
            pass # Expected
            
        print("4. Sending Request: GET /slow (High Latency)")
        await client.get("/slow", timeout=10.0)

async def check_logs():
    print("\n--- Verifying Database Content ---")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(APILog).order_by(APILog.timestamp.desc()).limit(5))
        logs = result.scalars().all()
        
        if not logs:
            print("❌ NO LOGS FOUND! Middleware failed.")
        else:
            print(f"✅ Found {len(logs)} logs.")
            for log in logs:
                print(f"   [{log.timestamp}] {log.method} {log.endpoint} -> {log.status_code} ({log.latency_ms:.2f}ms)")
                if log.error_message:
                    print(f"   ⚠️ Captured Error: {log.error_message}")

async def main():
    # Wait for server to be ready
    await asyncio.sleep(2) 
    await generate_traffic()
    
    # Wait a bit for background tasks to finish
    await asyncio.sleep(1)
    
    await check_logs()

if __name__ == "__main__":
    asyncio.run(main())
