"""Test suite for REMOTE API endpoints."""

import pytest
import requests
from tests.shared import APITestBase


class TestRemoteEndpoints(APITestBase):
    """Test REMOTE resource endpoints."""
    
    def get_resource_endpoints(self) -> list:
        """Get all GET endpoints for this resource."""
        return ['/remote/admin-urls/Query', '/remote/examinee-data/Query', '/remote/practice-checks/Query', '/remote/session-data/Query', '/remote/sessions/query', '/remote/system-checks/Query']
    
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

    def test_remote_admin_urls_query(self, auth_headers):
        """Test /remote/admin-urls/Query endpoint."""
        path = "/remote/admin-urls/Query"
        
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

    def test_remote_examinee_data_query(self, auth_headers):
        """Test /remote/examinee-data/Query endpoint."""
        path = "/remote/examinee-data/Query"
        
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

    def test_remote_practice_checks_query(self, auth_headers):
        """Test /remote/practice-checks/Query endpoint."""
        path = "/remote/practice-checks/Query"
        
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

    def test_remote_session_data_query(self, auth_headers):
        """Test /remote/session-data/Query endpoint."""
        path = "/remote/session-data/Query"
        
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

    def test_remote_sessions_query(self, auth_headers):
        """Test /remote/sessions/query endpoint."""
        path = "/remote/sessions/query"
        
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

    def test_remote_system_checks_query(self, auth_headers):
        """Test /remote/system-checks/Query endpoint."""
        path = "/remote/system-checks/Query"
        
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
