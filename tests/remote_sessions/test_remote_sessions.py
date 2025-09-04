"""Test suite for START-TEST API endpoints."""

import pytest
import requests
from tests.shared import APITestBase


class TestRemoteSessionsEndpoints(APITestBase):
    """Test START-TEST resource endpoints (POST operations)."""
    
    def get_remote_sessions_payload(self) -> dict:
        """Get the minimal viable payload for /remote/sessions endpoints."""
        return {
            "program-registration-id": "MIN001",
            "examinee": {
                "program-examinee-system-id": "MIN001", 
                "first-name": "Test",
                "last-name": "User"
            },
            "delivery": {
                "test-name": "MIN-TEST",
                "form-name": "MIN-FORM"
            }
        }
    
    def test_remote_sessions_start(self, auth_headers):
        """Test POST //remote/sessions/start endpoint with minimal viable payload."""
        path = "//remote/sessions/start"
        
        # Use program-id from environment or default to 52 (from your example)
        program_id = self.program_id or "52"
        query_params = {"program-id": program_id}
        
        # Get the minimal viable payload
        payload = self.get_remote_sessions_payload()
        
        # Make the POST request
        response = self.make_post_request(path, auth_headers, payload, query_params)
        
        # Assert successful response
        assert response.status_code == 200, (
            f"{path} returned {response.status_code}, expected 200. "
            f"Response: {response.text[:500]}"
        )
        
        # Verify response contains a start test URL
        response_text = response.text.strip()
        assert "starttest.com" in response_text, (
            f"{path} response should contain starttest.com URL. "
            f"Got: {response_text}"
        )
        
        # Log the response for verification
        print(f"\n{path}: {response.status_code}")
        print(f"Start test URL: {response_text}")

    def test_remote_sessions_login(self, auth_headers):
        """Test POST //remote/sessions/login endpoint with minimal viable payload."""
        path = "//remote/sessions/login"
        
        # Use program-id from environment or default to 52 (from your example)
        program_id = self.program_id or "52"
        query_params = {"program-id": program_id}
        
        # Use the minimal viable payload
        payload = self.get_remote_sessions_payload()
        
        # Make the POST request
        response = self.make_post_request(path, auth_headers, payload, query_params)
        
        # Assert successful response
        assert response.status_code == 200, (
            f"{path} returned {response.status_code}, expected 200. "
            f"Response: {response.text[:500]}"
        )
        
        # Verify response contains a login URL (might be different domain than start)
        response_text = response.text.strip()
        assert "http" in response_text and "://" in response_text, (
            f"{path} response should contain a URL. "
            f"Got: {response_text}"
        )
        
        # Log the response for verification
        print(f"\n{path}: {response.status_code}")
        print(f"Login URL: {response_text}")

    def get_resource_endpoints(self) -> list:
        """Get all POST endpoints for /remote/sessions resource."""
        return ["//remote/sessions/start", "//remote/sessions/login"]
