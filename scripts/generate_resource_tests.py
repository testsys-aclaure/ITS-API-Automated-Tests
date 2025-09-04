#!/usr/bin/env python3
"""Generate resource-specific test files from the unified test suite."""

import json
import os
import re
from pathlib import Path

def normalize_resource_name(resource: str) -> str:
    """Normalize resource names for consistent file naming."""
    # Handle case-insensitive duplicates
    resource_mapping = {
        'form': 'form',  # Combine /form and /Form
        'Form': 'form',
        'test': 'test',  # Combine /test and /Test  
        'Test': 'test',
        'user': 'user',  # Combine /user and /User
        'User': 'user',
        'event-class': 'event_class',  # Replace hyphens with underscores
        'iw-tool': 'iw_tool',
        'longitudinal-group': 'longitudinal_group',
        'message-history': 'message_history',
        'result-identifier': 'result_identifier',
        'secure-browser': 'secure_browser',
        'signalr-domain': 'signalr_domain',
        'start-test': 'start_test',
    }
    
    return resource_mapping.get(resource, resource.lower().replace('-', '_'))

def group_endpoints_by_resource() -> dict:
    """Group API endpoints by normalized resource name."""
    schema_path = Path(__file__).parent.parent / "schema" / "openapi.json"
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    resources = {}
    for path in spec['paths'].keys():
        parts = path.strip('/').split('/')
        if parts:
            resource = normalize_resource_name(parts[0])
            if resource not in resources:
                resources[resource] = []
            resources[resource].append(path)
    
    return resources

def extract_get_endpoints(spec: dict, resource_paths: list) -> list:
    """Extract GET endpoints for a specific resource."""
    get_endpoints = []
    for path in resource_paths:
        if 'get' in spec['paths'].get(path, {}):
            get_endpoints.append(path)
    return get_endpoints

def generate_test_file_content(resource: str, endpoints: list) -> str:
    """Generate the content for a resource-specific test file."""
    
    class_name = f"Test{resource.replace('_', '').title()}Endpoints"
    
    content = f'''"""Test suite for {resource.upper()} API endpoints."""

import pytest
import requests
from tests.shared import APITestBase


class {class_name}(APITestBase):
    """Test {resource.upper()} resource endpoints."""
    
    def get_resource_endpoints(self) -> list:
        """Get all GET endpoints for this resource."""
        return {endpoints}
    
    def get_endpoint_params(self, path: str) -> list:
        """Get query parameters for a specific endpoint."""
        params = []
        path_spec = self.spec['paths'].get(path, {{}})
        op_spec = path_spec.get('get', {{}})
        
        # Collect parameters from both path and operation levels
        for param_source in [path_spec.get('parameters', []), op_spec.get('parameters', [])]:
            for param in param_source:
                if isinstance(param, dict) and param.get('in') == 'query':
                    params.append(param['name'])
        
        return params
'''

    # Generate individual test methods for each endpoint
    for endpoint in endpoints:
        method_name = endpoint.replace('/', '_').replace('-', '_').lower().strip('_')
        content += f'''
    def test_{method_name}(self, auth_headers):
        """Test {endpoint} endpoint."""
        path = "{endpoint}"
        
        if self.should_skip_endpoint(path):
            pytest.skip(f"Skipping {{path}} - known to be problematic")
        
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
        print(f"\\n{{path}}: {{response.status_code}} - {{len(response.text)}} chars")
'''

    return content

def generate_resource_test_files():
    """Generate test files for each resource group."""
    resources = group_endpoints_by_resource()
    schema_path = Path(__file__).parent.parent / "schema" / "openapi.json"
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    tests_dir = Path(__file__).parent.parent / "tests"
    
    print("Generating resource-specific test files...")
    print("=" * 50)
    
    for resource, paths in sorted(resources.items()):
        # Only generate files for resources with GET endpoints
        get_endpoints = extract_get_endpoints(spec, paths)
        
        if not get_endpoints:
            print(f"Skipping {resource} - no GET endpoints")
            continue
            
        test_file = tests_dir / f"test_{resource}_endpoints.py"
        content = generate_test_file_content(resource, get_endpoints)
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Generated: {test_file.name:<35} ({len(get_endpoints)} GET endpoints)")
    
    print(f"\\nGenerated test files in: {tests_dir}")
    print("\\nTo run tests for a specific resource:")
    print("  pytest tests/test_event_endpoints.py -v")
    print("  pytest tests/test_examinee_endpoints.py -v")

if __name__ == "__main__":
    generate_resource_test_files()
