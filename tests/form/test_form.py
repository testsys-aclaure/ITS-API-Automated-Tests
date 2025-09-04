"""Test suite for FORM API endpoints."""

import pytest
import requests
from tests.shared import APITestBase


class TestFormEndpoints(APITestBase):
    """Test FORM resource endpoints."""
    
    def get_resource_endpoints(self) -> list:
        """Get all GET endpoints for this resource."""
        return ['/form/definition/Query', '/Form/Query', '/form/reports/Query', '/form/res-files/Query']
    
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

    def test_form_definition_query(self, auth_headers):
        """Test /form/definition/Query endpoint."""
        path = "/form/definition/Query"
        
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

    def test_form_query(self, auth_headers):
        """Test /Form/Query endpoint."""
        path = "/Form/Query"
        
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

    def test_form_reports_query(self, auth_headers):
        """Test /form/reports/Query endpoint."""
        path = "/form/reports/Query"
        
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

    def test_form_res_files_query(self, auth_headers):
        """Test /form/res-files/Query endpoint."""
        path = "/form/res-files/Query"
        
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
