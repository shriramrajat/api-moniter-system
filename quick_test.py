"""
Quick API Test Script
Run this to verify all endpoints are working
"""

import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(name, url, method="GET"):
    """Test a single endpoint"""
    try:
        print(f"\n{'='*60}")
        print(f"Testing: {name}")
        print(f"URL: {url}")
        
        if method == "GET":
            response = requests.get(url, timeout=5)
        
        print(f"Status Code: {response.status_code}")
        
        # Try to parse JSON
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)[:200]}...")
        except:
            print(f"Response (HTML): {response.text[:200]}...")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    print("🚀 API Monitoring System - Quick Test Suite")
    print("="*60)
    
    results = {}
    
    # Test basic endpoints
    results["Root"] = test_endpoint("Root Endpoint", f"{BASE_URL}/")
    time.sleep(0.5)
    
    results["Users"] = test_endpoint("Users Endpoint", f"{BASE_URL}/users")
    time.sleep(0.5)
    
    results["Slow"] = test_endpoint("Slow Endpoint", f"{BASE_URL}/slow")
    time.sleep(0.5)
    
    # Test error endpoint (should return 500)
    print(f"\n{'='*60}")
    print("Testing: Error Endpoint (Expected to fail)")
    try:
        response = requests.get(f"{BASE_URL}/error", timeout=5)
        results["Error"] = response.status_code == 500
        print(f"Status Code: {response.status_code} (Expected 500)")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        results["Error"] = False
    
    time.sleep(0.5)
    
    # Test analytics endpoints
    results["Logs"] = test_endpoint("Analytics - Logs", f"{BASE_URL}/analytics/logs?limit=5")
    time.sleep(0.5)
    
    results["Error Summary"] = test_endpoint("Analytics - Error Summary", f"{BASE_URL}/analytics/summary/errors")
    time.sleep(0.5)
    
    results["Latency Summary"] = test_endpoint("Analytics - Latency Summary", f"{BASE_URL}/analytics/summary/latency")
    time.sleep(0.5)
    
    results["AI Report"] = test_endpoint("Analytics - AI Incident Report", f"{BASE_URL}/analytics/incident-report")
    time.sleep(0.5)
    
    # Test dashboard
    print(f"\n{'='*60}")
    print("Testing: Dashboard")
    try:
        response = requests.get(f"{BASE_URL}/dashboard", timeout=5)
        results["Dashboard"] = response.status_code == 200 and "Dashboard" in response.text
        print(f"Status Code: {response.status_code}")
        print(f"Contains 'Dashboard': {'Dashboard' in response.text}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        results["Dashboard"] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("="*60)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above.")

if __name__ == "__main__":
    main()
