"""Test suite for EXAMINEE API endpoints (consolidated)."""

import pytest
import requests
from tests.shared import APITestBase


class TestExamineeEndpoints(APITestBase):
    """Test EXAMINEE resource endpoints (consolidated from sub-resources)."""
    
    def get_resource_endpoints(self) -> list:
        """Get all GET endpoints for this resource."""
        return [
            '/examinee/audit/query', 
            '/examinee/events/query', 
            '/examinee/longitudinal-segment-detail/query', 
            '/examinee/longitudinal-segments/query', 
            '/examinee/query', 
            '/examinee/record/query'
        ]
    
    def get_endpoint_params(self, path: str) -> list:
        """Get query parameters for a specific endpoint."""
        params = []
        path_spec = self.spec['paths'].get(path, {})
        op_spec = path_spec.get('get', {})
        
        # Collect parameters from both path and operation levels
        for param_source in [path_spec.get('parameters', []), op_spec.get('parameters', [])]:
            for param in param_source:
                if isinstance(param, dict) and param.get('in') == 'query':
                    params.append(param['name'])
        
        return params

    # GET endpoint tests
    def test_examinee_audit_query(self, auth_headers):
        """Test /examinee/audit/query endpoint."""
        path = "/examinee/audit/query"
        
        if self.should_skip_endpoint(path):
            pytest.skip(f"Skipping {path} - known to be problematic")
        
        # Get endpoint parameters and build query
        endpoint_params = self.get_endpoint_params(path)
        query_params = self.build_query_params(path, endpoint_params)
        
        # Make the request
        response = self.make_get_request(path, auth_headers, query_params)
        
        # Check expected status code
        expected_status_codes = self.get_expected_status_codes()
        expected_status = expected_status_codes.get(path, 200)
        
        # Assert response
        self.assert_response_success(response, path, expected_status)
        
        # Log the response for debugging
        print(f"\n{path}: {response.status_code} - {len(response.text)} chars")

    def test_examinee_events_query(self, auth_headers):
        """Test /examinee/events/query endpoint."""
        path = "/examinee/events/query"
        
        if self.should_skip_endpoint(path):
            pytest.skip(f"Skipping {path} - known to be problematic")
        
        # Get endpoint parameters and build query
        endpoint_params = self.get_endpoint_params(path)
        query_params = self.build_query_params(path, endpoint_params)
        
        # Make the request
        response = self.make_get_request(path, auth_headers, query_params)
        
        # Check expected status code
        expected_status_codes = self.get_expected_status_codes()
        expected_status = expected_status_codes.get(path, 200)
        
        # Assert response
        self.assert_response_success(response, path, expected_status)
        
        # Log the response for debugging
        print(f"\n{path}: {response.status_code} - {len(response.text)} chars")

    def test_examinee_longitudinal_segment_detail_query(self, auth_headers):
        """Test /examinee/longitudinal-segment-detail/query endpoint."""
        path = "/examinee/longitudinal-segment-detail/query"
        
        if self.should_skip_endpoint(path):
            pytest.skip(f"Skipping {path} - known to be problematic")
        
        # Use specific working parameters for this endpoint (from test_all_get_light.py)
        query_params = {
            "longitudinal-group-id": "1463",
            "examinee-id": "209058", 
            "program-id": "300"
        }
        
        # Make the request
        response = self.make_get_request(path, auth_headers, query_params)
        
        # Check expected status code
        expected_status_codes = self.get_expected_status_codes()
        expected_status = expected_status_codes.get(path, 200)
        
        # Assert response
        self.assert_response_success(response, path, expected_status)
        
        # Log the response for debugging
        print(f"\n{path}: {response.status_code} - {len(response.text)} chars")

    def test_examinee_longitudinal_segments_query(self, auth_headers):
        """Test /examinee/longitudinal-segments/query endpoint."""
        path = "/examinee/longitudinal-segments/query"
        
        if self.should_skip_endpoint(path):
            pytest.skip(f"Skipping {path} - known to be problematic")
        
        # Get endpoint parameters and build query
        endpoint_params = self.get_endpoint_params(path)
        query_params = self.build_query_params(path, endpoint_params)
        
        # Make the request
        response = self.make_get_request(path, auth_headers, query_params)
        
        # Check expected status code
        expected_status_codes = self.get_expected_status_codes()
        expected_status = expected_status_codes.get(path, 200)
        
        # Assert response
        self.assert_response_success(response, path, expected_status)
        
        # Log the response for debugging
        print(f"\n{path}: {response.status_code} - {len(response.text)} chars")

    def test_examinee_query(self, auth_headers):
        """Test /examinee/query endpoint."""
        path = "/examinee/query"
        
        if self.should_skip_endpoint(path):
            pytest.skip(f"Skipping {path} - known to be problematic")
        
        # Get endpoint parameters and build query
        endpoint_params = self.get_endpoint_params(path)
        query_params = self.build_query_params(path, endpoint_params)
        
        # Make the request
        response = self.make_get_request(path, auth_headers, query_params)
        
        # Check expected status code
        expected_status_codes = self.get_expected_status_codes()
        expected_status = expected_status_codes.get(path, 200)
        
        # Assert response
        self.assert_response_success(response, path, expected_status)
        
        # Log the response for debugging
        print(f"\n{path}: {response.status_code} - {len(response.text)} chars")

    def test_examinee_record_query(self, auth_headers):
        """Test /examinee/record/query endpoint."""
        path = "/examinee/record/query"
        
        if self.should_skip_endpoint(path):
            pytest.skip(f"Skipping {path} - known to be problematic")
        
        # Get endpoint parameters and build query
        endpoint_params = self.get_endpoint_params(path)
        query_params = self.build_query_params(path, endpoint_params)
        
        # Make the request
        response = self.make_get_request(path, auth_headers, query_params)
        
        # Check expected status code
        expected_status_codes = self.get_expected_status_codes()
        expected_status = expected_status_codes.get(path, 200)
        
        # Assert response
        self.assert_response_success(response, path, expected_status)
        
        # Log the response for debugging
        print(f"\n{path}: {response.status_code} - {len(response.text)} chars")

    # POST/PATCH/DELETE endpoint payload methods
    def get_event_examinee_import_payload(self) -> dict:
        """Get the minimal viable payload for /event/examinee/import endpoints."""
        return {
            "examinees": [
                {
                    "program-examinee-system-id": "MIN001", 
                    "first-name": "Test",
                    "last-name": "User"
                }
            ]
        }
    
    def get_examinee_import_payload(self) -> dict:
        """Get the minimal viable payload for /examinee/import endpoints."""
        return {
            "examinees": [
                {
                    "program-examinee-system-id": "MIN001", 
                    "first-name": "Test",
                    "last-name": "User"
                }
            ]
        }

    # POST/PATCH/DELETE endpoint tests (from consolidated sub-resources)
    def test_event_examinee_import_post(self, auth_headers):
        """Test POST /event/examinee/import endpoint."""
        path = "/event/examinee/import"
        
        # Use program-id from environment or default to 52
        program_id = self.program_id or "52"
        query_params = {"program-id": program_id, "event-id": "1"}
        
        # Get the minimal viable payload
        payload = self.get_event_examinee_import_payload()
        
        # Make the POST request
        response = self.make_post_request(path, auth_headers, payload, query_params)
        
        # Assert successful response (could be 200 or 422 for missing data)
        assert response.status_code in [200, 422], (
            f"{path} returned {response.status_code}, expected 200 or 422. "
            f"Response: {response.text[:500]}"
        )
        
        # Log the response for verification
        print(f"\n{path} POST: {response.status_code} - {len(response.text)} chars")

    def test_event_examinee_import_patch(self, auth_headers):
        """Test PATCH /event/examinee/import endpoint."""
        path = "/event/examinee/import"
        
        # Use program-id from environment or default to 52
        program_id = self.program_id or "52"
        query_params = {"program-id": program_id, "event-id": "1"}
        
        # Get the minimal viable payload
        payload = self.get_event_examinee_import_payload()
        
        # Make the PATCH request using requests directly
        url = f"{self.base_url}{path}"
        response = requests.patch(
            url, 
            headers=auth_headers, 
            json=payload, 
            params=query_params,
            timeout=30
        )
        
        # Assert successful response (could be 200 or 422 for missing data)
        assert response.status_code in [200, 422], (
            f"{path} returned {response.status_code}, expected 200 or 422. "
            f"Response: {response.text[:500]}"
        )
        
        # Log the response for verification
        print(f"\n{path} PATCH: {response.status_code} - {len(response.text)} chars")

    def test_examinee_import_post(self, auth_headers):
        """Test POST /examinee/import endpoint."""
        path = "/examinee/import"
        
        # Use program-id from environment or default to 52
        program_id = self.program_id or "52"
        query_params = {"program-id": program_id}
        
        # Get the minimal viable payload
        payload = self.get_examinee_import_payload()
        
        # Make the POST request
        response = self.make_post_request(path, auth_headers, payload, query_params)
        
        # Assert successful response (could be 200 or 422 for missing data)
        assert response.status_code in [200, 422], (
            f"{path} returned {response.status_code}, expected 200 or 422. "
            f"Response: {response.text[:500]}"
        )
        
        # Log the response for verification
        print(f"\n{path} POST: {response.status_code} - {len(response.text)} chars")

    def test_examinee_import_patch(self, auth_headers):
        """Test PATCH /examinee/import endpoint."""
        path = "/examinee/import"
        
        # Use program-id from environment or default to 52
        program_id = self.program_id or "52"
        query_params = {"program-id": program_id}
        
        # Get the minimal viable payload
        payload = self.get_examinee_import_payload()
        
        # Make the PATCH request using requests directly
        url = f"{self.base_url}{path}"
        response = requests.patch(
            url, 
            headers=auth_headers, 
            json=payload, 
            params=query_params,
            timeout=30
        )
        
        # Assert successful response (could be 200 or 422 for missing data)
        assert response.status_code in [200, 422], (
            f"{path} returned {response.status_code}, expected 200 or 422. "
            f"Response: {response.text[:500]}"
        )
        
        # Log the response for verification
        print(f"\n{path} PATCH: {response.status_code} - {len(response.text)} chars")

    def test_examinee_delete(self, auth_headers):
        """Test DELETE /examinee/delete endpoint."""
        path = "/examinee/delete"
        
        # Use program-id from environment or default to 52
        program_id = self.program_id or "52"
        query_params = {
            "program-id": program_id,
            "program-examinee-system-id": "NONEXISTENT_USER_FOR_DELETE_TEST"
        }
        
        # Make the DELETE request using requests directly
        url = f"{self.base_url}{path}"
        response = requests.delete(
            url, 
            headers=auth_headers, 
            params=query_params,
            timeout=30
        )
        
        # Assert response (could be 200 if deleted, 404 if not found, or 422 for missing data)
        assert response.status_code in [200, 404, 422], (
            f"{path} returned {response.status_code}, expected 200, 404, or 422. "
            f"Response: {response.text[:500]}"
        )
        
        # Log the response for verification
        print(f"\n{path} DELETE: {response.status_code} - {len(response.text)} chars")
