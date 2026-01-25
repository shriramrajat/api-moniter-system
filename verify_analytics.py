import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000/analytics"

async def test_analytics():
    async with httpx.AsyncClient(timeout=10.0) as client:
        print("\n--- 1. Testing Raw Logs (/logs) ---")
        response = await client.get(f"{BASE_URL}/logs?limit=5")
        if response.status_code == 200:
            logs = response.json()
            print(f"✅ Retrieved {len(logs)} logs.")
            for l in logs:
                print(f"   - {l['method']} {l['endpoint']} ({l['status_code']})")
        else:
            print(f"❌ Failed: {response.text}")

        print("\n--- 2. Testing Latency Summary (/summary/latency) ---")
        response = await client.get(f"{BASE_URL}/summary/latency")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Latency Stats:")
            for s in stats:
                print(f"   - {s['endpoint']}: Avg {s['avg_latency']}ms (Max {s['max_latency']}ms)")
        else:
            print(f"❌ Failed: {response.text}")

        print("\n--- 3. Testing Error Summary (/summary/errors) ---")
        response = await client.get(f"{BASE_URL}/summary/errors")
        if response.status_code == 200:
            errors = response.json()
            print("✅ Error Stats:")
            for e in errors:
                print(f"   - {e['endpoint']}: {e['error_count']} errors")
        else:
            print(f"❌ Failed: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_analytics())
