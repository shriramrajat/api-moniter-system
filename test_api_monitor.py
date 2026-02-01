"""
Test Suite for API Monitoring System

This file contains basic tests to verify the core functionality.
Run with: pytest test_api_monitor.py
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
import asyncio

client = TestClient(app)


class TestBasicEndpoints:
    """Test basic API endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns operational status"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "System Operational"}
    
    def test_users_endpoint(self):
        """Test the users endpoint returns data"""
        response = client.get("/users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
    
    def test_error_endpoint(self):
        """Test that error endpoint properly handles exceptions"""
        response = client.get("/error")
        assert response.status_code == 500
    
    def test_slow_endpoint(self):
        """Test slow endpoint completes successfully"""
        response = client.get("/slow")
        assert response.status_code == 200
        assert "slow" in response.json()["message"].lower()


class TestAnalyticsEndpoints:
    """Test analytics and monitoring endpoints"""
    
    def test_get_logs(self):
        """Test retrieving logs"""
        response = client.get("/analytics/logs?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_logs_with_filters(self):
        """Test retrieving logs with status code filter"""
        response = client.get("/analytics/logs?status_code=200&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_error_summary(self):
        """Test error summary endpoint"""
        response = client.get("/analytics/summary/errors")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_latency_summary(self):
        """Test latency summary endpoint"""
        response = client.get("/analytics/summary/latency")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_ai_incident_report(self):
        """Test AI incident report endpoint"""
        response = client.get("/analytics/incident-report")
        assert response.status_code == 200
        data = response.json()
        assert "report" in data


class TestDashboard:
    """Test dashboard functionality"""
    
    def test_dashboard_loads(self):
        """Test that dashboard HTML loads successfully"""
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "API Monitor Dashboard" in response.text


class TestMiddleware:
    """Test logging middleware functionality"""
    
    def test_middleware_logs_requests(self):
        """Test that middleware logs all requests"""
        # Make a request
        response = client.get("/users")
        assert response.status_code == 200
        
        # Check if it was logged (should appear in recent logs)
        logs_response = client.get("/analytics/logs?limit=10")
        logs = logs_response.json()
        
        # Verify at least one log entry exists
        assert len(logs) > 0
    
    def test_middleware_captures_errors(self):
        """Test that middleware captures error information"""
        # Trigger an error
        response = client.get("/error")
        assert response.status_code == 500
        
        # Check error logs
        logs_response = client.get("/analytics/logs?status_code=500&limit=10")
        error_logs = logs_response.json()
        
        # Should have error entries
        assert len(error_logs) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
