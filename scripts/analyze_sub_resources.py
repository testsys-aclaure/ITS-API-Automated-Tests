#!/usr/bin/env python3
"""Analyze API endpoints for sub-resource pipeline organization."""

import json
from pathlib import Path
from collections import defaultdict

def get_sub_resource_groups():
    """Group endpoints by sub-resource paths (before /query, /create, etc.)."""
    schema_path = Path(__file__).parent.parent / "schema" / "openapi.json"
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    # Common endpoint action patterns
    action_patterns = {
        'query', 'create', 'delete', 'update', 'import', 'export', 'upload', 
        'start', 'login', 'validate', 'close', 'Query', 'Create', 'Delete', 
        'Update', 'Import', 'Export', 'Upload', 'Start', 'Login', 'Validate'
    }
    
    sub_resources = defaultdict(list)
    
    for path in spec['paths'].keys():
        parts = path.strip('/').split('/')
        
        # Build the sub-resource path (everything before the action)
        sub_resource_parts = []
        
        for i, part in enumerate(parts):
            if part in action_patterns:
                # Stop here - this is an action
                break
            sub_resource_parts.append(part)
        
        # Create the sub-resource key
        if sub_resource_parts:
            sub_resource_key = '/'.join(sub_resource_parts)
            sub_resources[sub_resource_key].append(path)
    
    return sub_resources

def normalize_pipeline_name(sub_resource: str) -> str:
    """Convert sub-resource path to pipeline name."""
    # Replace special characters and make lowercase
    normalized = sub_resource.lower()
    normalized = normalized.replace('/', '_')
    normalized = normalized.replace('-', '_')
    return normalized

def analyze_sub_resource_pipelines():
    """Analyze and display sub-resource pipeline organization."""
    sub_resources = get_sub_resource_groups()
    
    print("🔍 Sub-Resource Pipeline Analysis:")
    print("=" * 60)
    
    pipeline_count = 0
    total_endpoints = 0
    
    for sub_resource, paths in sorted(sub_resources.items()):
        pipeline_name = normalize_pipeline_name(sub_resource)
        endpoint_count = len(paths)
        pipeline_count += 1
        total_endpoints += endpoint_count
        
        print(f"{pipeline_count:2d}. {pipeline_name:<35} ({endpoint_count:2d} endpoints)")
        print(f"    Sub-resource: /{sub_resource}")
        
        # Show the actual endpoints
        for path in sorted(paths):
            print(f"      {path}")
        print()
    
    print("=" * 60)
    print(f"📊 SUMMARY:")
    print(f"   Total Pipelines: {pipeline_count}")
    print(f"   Total Endpoints: {total_endpoints}")
    
    return sub_resources

def generate_pipeline_structure():
    """Generate the complete pipeline structure."""
    sub_resources = get_sub_resource_groups()
    
    print(f"\\n🚀 Complete Pipeline Structure:")
    print("=" * 60)
    
    for sub_resource, paths in sorted(sub_resources.items()):
        pipeline_name = normalize_pipeline_name(sub_resource)
        endpoint_count = len(paths)
        
        print(f"{pipeline_name}-validation.yml → tests/{pipeline_name}/ ({endpoint_count} endpoints)")
    
    print(f"\\nSuggested folder structure:")
    print("tests/")
    print("├── shared/")
    
    for sub_resource in sorted(sub_resources.keys()):
        pipeline_name = normalize_pipeline_name(sub_resource)
        print(f"├── {pipeline_name}/")
        print(f"│   └── test_endpoints.py")
    
    return sub_resources

if __name__ == "__main__":
    print("🎯 Sub-Resource Pipeline Organization Tool")
    print("Analyzing endpoints for fine-grained pipeline separation")
    print("=" * 70)
    
    sub_resources = analyze_sub_resource_pipelines()
    generate_pipeline_structure()
    
    print(f"\\n✅ Analysis complete!")
    print(f"\\nEach sub-resource path becomes its own pipeline:")
    print(f"  /examinee → examinee-validation.yml")
    print(f"  /examinee/events → examinee_events-validation.yml")
    print(f"  /examinee/longitudinal-segments → examinee_longitudinal_segments-validation.yml")
    print(f"  etc.")
