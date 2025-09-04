#!/usr/bin/env python3
"""Analyze OpenAPI schema to identify resource groupings for test organization."""

import json
import os

def analyze_resources():
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "schema", "openapi.json")
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)

    # Group endpoints by resource
    resources = {}
    for path in spec['paths'].keys():
        # Extract the primary resource from the path
        parts = path.strip('/').split('/')
        if parts:
            resource = parts[0]
            if resource not in resources:
                resources[resource] = []
            resources[resource].append(path)

    # Print resource groups
    print("API Resource Groups Analysis:")
    print("=" * 50)
    
    total_endpoints = 0
    for resource, paths in sorted(resources.items()):
        total_endpoints += len(paths)
        print(f"\n{resource.upper()}: {len(paths)} endpoints")
        for path in sorted(paths):
            # Show HTTP methods for each path
            methods = list(spec['paths'][path].keys())
            methods = [m.upper() for m in methods if m != 'parameters']
            print(f"  {path} [{', '.join(methods)}]")
    
    print(f"\nTotal: {total_endpoints} endpoints across {len(resources)} resource groups")
    
    # Suggest test file organization
    print("\nSuggested Test File Organization:")
    print("=" * 50)
    
    for resource in sorted(resources.keys()):
        test_file = f"test_{resource}_endpoints.py"
        endpoint_count = len(resources[resource])
        print(f"tests/{test_file:<30} ({endpoint_count} endpoints)")

if __name__ == "__main__":
    analyze_resources()
