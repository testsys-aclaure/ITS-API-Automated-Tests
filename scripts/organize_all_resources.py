#!/usr/bin/env python3
"""Complete resource organization script based on OpenAPI spec."""

import json
import os
from pathlib import Path

def normalize_resource_name(resource: str) -> str:
    """Normalize resource names for consistent folder naming."""
    # Handle case-insensitive duplicates and normalize names
    resource_mapping = {
        'Form': 'form',  # Combine /Form and /form
        'form': 'form',
        'Test': 'test',  # Combine /Test and /test  
        'test': 'test',
        'User': 'user',  # Combine /User and /user
        'user': 'user',
        'Timezone': 'timezone',  # Combine /Timezone
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

def get_all_resources_from_openapi():
    """Get all resource groups from OpenAPI spec."""
    schema_path = Path(__file__).parent.parent / "schema" / "openapi.json"
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    resources = {}
    for path in spec['paths'].keys():
        parts = path.strip('/').split('/')
        if parts:
            original_resource = parts[0]
            normalized_resource = normalize_resource_name(original_resource)
            
            if normalized_resource not in resources:
                resources[normalized_resource] = {
                    'paths': [],
                    'original_names': set()
                }
            
            resources[normalized_resource]['paths'].append(path)
            resources[normalized_resource]['original_names'].add(original_resource)
    
    return resources

def create_missing_resource_folders():
    """Create folders for any missing resources."""
    resources = get_all_resources_from_openapi()
    tests_dir = Path(__file__).parent.parent / "tests"
    
    existing_folders = {d.name for d in tests_dir.iterdir() if d.is_dir() and d.name != '__pycache__' and d.name != 'shared'}
    
    print("🔍 Resource Analysis:")
    print("=" * 50)
    
    created_folders = []
    
    for resource, info in sorted(resources.items()):
        endpoint_count = len(info['paths'])
        original_names = ', '.join(sorted(info['original_names']))
        
        print(f"{resource:<20} ({endpoint_count:2d} endpoints) - Original: {original_names}")
        
        resource_dir = tests_dir / resource
        if resource not in existing_folders:
            # Create the folder
            resource_dir.mkdir(exist_ok=True)
            
            # Create __init__.py
            init_file = resource_dir / "__init__.py"
            init_file.write_text("# Make package importable\\n")
            
            created_folders.append(resource)
            print(f"  ✅ Created: tests/{resource}/")
        else:
            print(f"  ✅ Exists:  tests/{resource}/")
    
    print(f"\\n📁 Total Resources: {len(resources)}")
    print(f"📁 Created Folders: {len(created_folders)}")
    
    if created_folders:
        print(f"\\n🆕 New folders created:")
        for folder in created_folders:
            print(f"  - tests/{folder}/")
    
    # Show any existing folders that might not match resources
    all_resource_names = set(resources.keys())
    extra_folders = existing_folders - all_resource_names
    
    if extra_folders:
        print(f"\\n⚠️  Folders not matching OpenAPI resources:")
        for folder in sorted(extra_folders):
            print(f"  - tests/{folder}/")
    
    return resources

def generate_complete_pipeline_list():
    """Generate a complete list of all possible pipelines."""
    resources = get_all_resources_from_openapi()
    
    print(f"\\n🚀 Complete Azure Pipeline Configuration:")
    print("=" * 50)
    
    for resource in sorted(resources.keys()):
        endpoint_count = len(resources[resource]['paths'])
        print(f"{resource}-validation.yml → tests/{resource}/ ({endpoint_count} endpoints)")
    
    print(f"\\nTotal: {len(resources)} separate resource validation pipelines")

if __name__ == "__main__":
    print("🔧 Complete Resource Organization Tool")
    print("=" * 60)
    
    resources = create_missing_resource_folders()
    generate_complete_pipeline_list()
    
    print(f"\\n✅ Organization complete!")
    print(f"\\nTo test individual resources:")
    for resource in sorted(list(resources.keys())[:5]):  # Show first 5 as examples
        print(f"  pytest tests/{resource}/ -v")
    print(f"  ... and {len(resources)-5} more resources")
    
    print(f"\\nTo test all resources:")
    print(f"  pytest tests/ -v")
