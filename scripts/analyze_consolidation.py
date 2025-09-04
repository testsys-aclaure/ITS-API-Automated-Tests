#!/usr/bin/env python3
"""
🔍 Analyze Pipeline Consolidation Opportunities
Identifies resources that should be consolidated into single pipelines
"""

import json
from pathlib import Path
from collections import defaultdict

def load_openapi_spec():
    """Load and parse the OpenAPI specification"""
    with open("schema/openapi.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_consolidation_opportunities():
    """Find resources that should be consolidated"""
    spec = load_openapi_spec()
    
    # Group endpoints by their logical resource (before first sub-path)
    resource_groups = defaultdict(list)
    
    for path in spec['paths']:
        # Extract the main resource (first part after /)
        parts = path.strip('/').split('/')
        if len(parts) >= 2:
            main_resource = parts[0]
            resource_groups[main_resource].append(path)
    
    print("🔍 Pipeline Consolidation Analysis")
    print("=" * 60)
    
    consolidation_opportunities = []
    
    for main_resource, endpoints in resource_groups.items():
        if len(endpoints) > 1:
            # Check if we currently have this split across multiple pipelines
            sub_resources = set()
            for endpoint in endpoints:
                parts = endpoint.strip('/').split('/')
                if len(parts) >= 3:
                    # Has sub-resource (e.g., /secure-browser/errors vs /secure-browser/tokens)
                    sub_resource = f"{parts[0]}-{parts[1]}"
                    sub_resources.add(sub_resource)
                else:
                    # No sub-resource
                    sub_resources.add(parts[0])
            
            if len(sub_resources) > 1:
                # Currently split, might need consolidation
                consolidation_opportunities.append({
                    'main_resource': main_resource,
                    'endpoints': endpoints,
                    'current_pipelines': list(sub_resources),
                    'should_consolidate': True
                })
                
                print(f"\n🎯 {main_resource.upper()} Resource:")
                print(f"   Endpoints: {len(endpoints)}")
                for endpoint in sorted(endpoints):
                    print(f"     - {endpoint}")
                print(f"   Current pipelines: {len(sub_resources)}")
                for pipeline in sorted(sub_resources):
                    print(f"     - {pipeline}-validation.yml")
                print(f"   ✅ Should consolidate into: {main_resource}-validation.yml")
    
    return consolidation_opportunities

def suggest_folder_consolidation():
    """Suggest which test folders should be consolidated"""
    
    consolidations = {
        'secure-browser': {
            'folders_to_merge': ['secure_browser_errors', 'secure_browser_tokens'],
            'target_folder': 'secure_browser',
            'endpoints': ['/secure-browser/errors/query', '/secure-browser/tokens/validate']
        },
        # Add other consolidations as we find them
    }
    
    print("\n" + "=" * 60)
    print("📁 Folder Consolidation Recommendations:")
    print("=" * 60)
    
    for resource, config in consolidations.items():
        print(f"\n🔧 {resource.upper()}:")
        print(f"   Current folders: {', '.join(config['folders_to_merge'])}")
        print(f"   Target folder: {config['target_folder']}")
        print(f"   Endpoints ({len(config['endpoints'])}):")
        for endpoint in config['endpoints']:
            print(f"     - {endpoint}")
        print(f"   Pipeline: {resource}-validation.yml")

def main():
    """Main analysis"""
    opportunities = analyze_consolidation_opportunities()
    suggest_folder_consolidation()
    
    print(f"\n📊 SUMMARY:")
    print(f"   Consolidation opportunities found: {len(opportunities)}")
    print(f"   This will reduce pipeline complexity")
    print(f"   Logical grouping by main resource")

if __name__ == "__main__":
    main()
