#!/usr/bin/env python3
"""Analyze schema to find minimum required fields for start-test endpoints."""

import json
from pathlib import Path

def analyze_schema(schema_name, components):
    schema = components['schemas'][schema_name]
    print(f'=== {schema_name} ===')
    
    required_fields = schema.get('required', [])
    if required_fields:
        print(f'Required fields: {required_fields}')
    else:
        print('Required fields: None specified')
    
    if 'properties' in schema:
        print('All properties:')
        for prop, details in schema['properties'].items():
            prop_type = details.get('type', 'unknown')
            is_required = prop in required_fields
            is_readonly = details.get('readOnly', False)
            is_nullable = details.get('nullable', False)
            has_ref = '$ref' in details
            
            status = []
            if is_required: 
                status.append('REQUIRED')
            if is_readonly: 
                status.append('readonly')
            if is_nullable: 
                status.append('nullable')
            if has_ref: 
                ref_name = details['$ref'].split('/')[-1]
                status.append(f'ref: {ref_name}')
            
            status_str = f' [{", ".join(status)}]' if status else ''
            print(f'  {prop}: {prop_type}{status_str}')
    print()

def create_minimal_payload(components):
    """Create the absolute minimum payload based on required fields."""
    
    # Check what's actually required in StartTestDataHolder
    main_schema = components['schemas']['StartTestDataHolder']
    required_main = main_schema.get('required', [])
    
    payload = {}
    
    # Only add required fields
    for field in required_main:
        if field == 'examinee':
            # Check what's required in Examinee3
            examinee_schema = components['schemas']['Examinee3']
            required_examinee = examinee_schema.get('required', [])
            
            if required_examinee:
                examinee = {}
                for req_field in required_examinee:
                    if req_field in ['first-name', 'last-name']:
                        examinee[req_field] = 'Test'
                    elif req_field == 'program-examinee-system-id':
                        examinee[req_field] = 'MIN001'
                    else:
                        examinee[req_field] = 'test-value'
                payload['examinee'] = examinee
            else:
                # No required fields in examinee, but may need minimal structure
                payload['examinee'] = {}
        
        elif field == 'delivery':
            # Check what's required in StartTestDelivery
            delivery_schema = components['schemas']['StartTestDelivery']
            required_delivery = delivery_schema.get('required', [])
            
            if required_delivery:
                delivery = {}
                for req_field in required_delivery:
                    if req_field in ['test-name', 'form-name']:
                        delivery[req_field] = 'MIN-TEST'
                    else:
                        delivery[req_field] = 'test-value'
                payload['delivery'] = delivery
            else:
                payload['delivery'] = {}
        
        elif field == 'program-registration-id':
            payload['program-registration-id'] = 'MIN001'
        
        elif field == 'start-test-options':
            payload['start-test-options'] = 0
        
        else:
            payload[field] = 'test-value'
    
    return payload

def main():
    schema_path = Path(__file__).parent.parent / "schema" / "openapi.json"
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    components = spec['components']
    
    # Analyze the schemas
    analyze_schema('StartTestDataHolder', components)
    analyze_schema('Examinee3', components)
    analyze_schema('StartTestDelivery', components)
    
    # Create minimal payload
    print('=== MINIMAL VIABLE PAYLOAD ===')
    minimal = create_minimal_payload(components)
    if minimal:
        print('Based on schema analysis:')
        print(json.dumps(minimal, indent=2))
    else:
        print('No required fields found - empty payload should work!')
        print('{}')

if __name__ == "__main__":
    main()
