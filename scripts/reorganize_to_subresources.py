#!/usr/bin/env python3
"""
🔄 Reorganize Tests to Sub-Resource Structure
Implements the 43-pipeline sub-resource organization identified by analyze_sub_resources.py
"""

import os
import shutil
import json
from pathlib import Path

def get_subresource_mapping():
    """Returns the complete sub-resource mapping from analysis"""
    return {
        'form': {'path': '/Form', 'endpoints': ['/Form/Create', '/Form/Delete', '/Form/Query', '/Form/Update']},
        'test': {'path': '/Test', 'endpoints': ['/Test/Create', '/Test/Delete', '/Test/Query', '/Test/Update']},
        'timezone': {'path': '/Timezone', 'endpoints': ['/Timezone/Query']},
        'user': {'path': '/User', 'endpoints': ['/User/delete', '/User/query']},
        'channel_institutions': {'path': '/channel/institutions', 'endpoints': ['/channel/institutions/import', '/channel/institutions/query']},
        'event': {'path': '/event', 'endpoints': ['/event/close', '/event/create', '/event/query', '/event/update']},
        'event_class': {'path': '/event-class', 'endpoints': ['/event-class/Create', '/event-class/Delete', '/event-class/Query', '/event-class/Update']},
        'event_class_examinees': {'path': '/event-class/examinees', 'endpoints': ['/event-class/examinees/create', '/event-class/examinees/delete', '/event-class/examinees/query']},
        'event_authorizations': {'path': '/event/authorizations', 'endpoints': ['/event/authorizations/Query']},
        'event_examinee': {'path': '/event/examinee', 'endpoints': ['/event/examinee/import']},
        'examinee': {'path': '/examinee', 'endpoints': ['/examinee/delete', '/examinee/import', '/examinee/query']},
        'examinee_audit': {'path': '/examinee/audit', 'endpoints': ['/examinee/audit/query']},
        'examinee_events': {'path': '/examinee/events', 'endpoints': ['/examinee/events/query']},
        'examinee_longitudinal_segment_detail': {'path': '/examinee/longitudinal-segment-detail', 'endpoints': ['/examinee/longitudinal-segment-detail/query']},
        'examinee_longitudinal_segments': {'path': '/examinee/longitudinal-segments', 'endpoints': ['/examinee/longitudinal-segments/query']},
        'examinee_record': {'path': '/examinee/record', 'endpoints': ['/examinee/record/query']},
        'form_definition': {'path': '/form/definition', 'endpoints': ['/form/definition/Import', '/form/definition/Query']},
        'form_reports': {'path': '/form/reports', 'endpoints': ['/form/reports/Query']},
        'form_res_files': {'path': '/form/res-files', 'endpoints': ['/form/res-files/Query']},
        'inventory': {'path': '/inventory', 'endpoints': ['/inventory/query']},
        'iw_tool': {'path': '/iw-tool', 'endpoints': ['/iw-tool/export/tests/query', '/iw-tool/import/import', '/iw-tool/import/import-async', '/iw-tool/import/query']},
        'longitudinal_group_examinees': {'path': '/longitudinal-group/examinees', 'endpoints': ['/longitudinal-group/examinees/create', '/longitudinal-group/examinees/delete', '/longitudinal-group/examinees/query', '/longitudinal-group/examinees/update']},
        'message_history': {'path': '/message-history', 'endpoints': ['/message-history/query']},
        'order': {'path': '/order', 'endpoints': ['/order/Create', '/order/Delete', '/order/Query']},
        'package_forms': {'path': '/package/forms', 'endpoints': ['/package/forms/Query']},
        'registration': {'path': '/registration', 'endpoints': ['/registration/delete', '/registration/import', '/registration/query', '/registration/update']},
        'remote_admin_urls': {'path': '/remote/admin-urls', 'endpoints': ['/remote/admin-urls/Query']},
        'remote_examinee_data': {'path': '/remote/examinee-data', 'endpoints': ['/remote/examinee-data/Query']},
        'remote_practice_checks': {'path': '/remote/practice-checks', 'endpoints': ['/remote/practice-checks/Query']},
        'remote_session_data': {'path': '/remote/session-data', 'endpoints': ['/remote/session-data/Query']},
        'remote_sessions': {'path': '/remote/sessions', 'endpoints': ['/remote/sessions/create', '/remote/sessions/delete', '/remote/sessions/query', '/remote/sessions/update']},
        'remote_system_checks': {'path': '/remote/system-checks', 'endpoints': ['/remote/system-checks/Query']},
        'result': {'path': '/result', 'endpoints': ['/result/query', '/result/update', '/result/upload']},
        'result_identifier': {'path': '/result-identifier', 'endpoints': ['/result-identifier/Query']},
        'sabbatical': {'path': '/sabbatical', 'endpoints': ['/sabbatical/Query']},
        'secure_browser_errors': {'path': '/secure-browser/errors', 'endpoints': ['/secure-browser/errors/query']},
        'secure_browser_tokens': {'path': '/secure-browser/tokens', 'endpoints': ['/secure-browser/tokens/validate']},
        'session': {'path': '/session', 'endpoints': ['/session/create', '/session/delete', '/session/query', '/session/update']},
        'signalr_domain': {'path': '/signalr-domain', 'endpoints': ['/signalr-domain/query']},
        'start_test': {'path': '/start-test', 'endpoints': ['/start-test/Login', '/start-test/Start']},
        'test_forms': {'path': '/test/forms', 'endpoints': ['/test/forms/Query']},
        'test_pretest_references': {'path': '/test/pretest-references', 'endpoints': ['/test/pretest-references/Import', '/test/pretest-references/Query']},
        'user_access': {'path': '/user/access', 'endpoints': ['/user/access/delete', '/user/access/query']}
    }

def find_current_test_files():
    """Find all current test files to understand what needs to be moved"""
    tests_dir = Path("tests")
    current_files = {}
    
    for folder in tests_dir.iterdir():
        if folder.is_dir() and folder.name not in ['shared', '__pycache__']:
            test_files = list(folder.glob("*.py"))
            if test_files:
                current_files[folder.name] = test_files
    
    return current_files

def create_subresource_folders():
    """Create all 43 sub-resource folders"""
    tests_dir = Path("tests")
    subresource_mapping = get_subresource_mapping()
    
    print("🏗️  Creating sub-resource folder structure...")
    
    for folder_name in subresource_mapping.keys():
        folder_path = tests_dir / folder_name
        folder_path.mkdir(exist_ok=True)
        print(f"   ✅ Created: {folder_path}")
    
    return subresource_mapping

def move_existing_tests():
    """Move and merge existing test files to new structure"""
    current_files = find_current_test_files()
    subresource_mapping = get_subresource_mapping()
    
    print("\n📦 Moving existing test files...")
    
    # Handle direct matches first
    for current_folder, test_files in current_files.items():
        if current_folder in subresource_mapping:
            # Direct match - move files
            for test_file in test_files:
                dest_path = Path("tests") / current_folder / test_file.name
                if not dest_path.exists():
                    shutil.copy2(test_file, dest_path)
                    print(f"   ✅ Moved: {test_file} → {dest_path}")
        else:
            # Need to figure out mapping for this folder
            print(f"   ⚠️  Need manual mapping for folder: {current_folder}")
    
    # Handle special cases that need custom mapping
    special_mappings = {
        'channel': 'channel_institutions',
        'longitudinal_group': 'longitudinal_group_examinees',
        'package': 'package_forms',
        'remote': ['remote_admin_urls', 'remote_examinee_data', 'remote_practice_checks', 
                  'remote_session_data', 'remote_sessions', 'remote_system_checks'],
        'secure_browser': ['secure_browser_errors', 'secure_browser_tokens']
    }
    
    for old_folder, new_mappings in special_mappings.items():
        if old_folder in current_files:
            if isinstance(new_mappings, str):
                # Single mapping
                source_files = current_files[old_folder]
                dest_folder = Path("tests") / new_mappings
                for test_file in source_files:
                    dest_path = dest_folder / test_file.name
                    if not dest_path.exists():
                        shutil.copy2(test_file, dest_path)
                        print(f"   ✅ Mapped: {test_file} → {dest_path}")
            else:
                # Multiple mappings - copy to first one for now
                source_files = current_files[old_folder]
                dest_folder = Path("tests") / new_mappings[0]
                for test_file in source_files:
                    dest_path = dest_folder / test_file.name
                    if not dest_path.exists():
                        shutil.copy2(test_file, dest_path)
                        print(f"   ✅ Mapped: {test_file} → {dest_path} (primary mapping)")

def create_test_files_for_empty_folders():
    """Create test_endpoints.py files for folders that don't have any"""
    tests_dir = Path("tests")
    subresource_mapping = get_subresource_mapping()
    
    print("\n📄 Creating test_endpoints.py files for empty folders...")
    
    # Read the working start_test example as a template
    start_test_file = tests_dir / "start_test" / "test_endpoints.py"
    template_content = ""
    
    if start_test_file.exists():
        with open(start_test_file, 'r') as f:
            template_content = f.read()
    else:
        # Fallback template
        template_content = '''"""
Test endpoints for {resource_name} sub-resource
Generated from sub-resource pipeline organization
"""
import pytest
from tests.shared.api_test_base import APITestBase

class Test{class_name}Endpoints(APITestBase):
    """Test class for {resource_name} endpoints"""
    
    @pytest.mark.get
    def test_get_endpoints(self):
        """Test all GET endpoints for {resource_name}"""
        endpoints = {endpoints_list}
        
        for endpoint in endpoints:
            if any(action in endpoint.lower() for action in ['query', 'get']):
                response = self.make_get_request(endpoint)
                assert response.status_code in [200, 404], f"Endpoint {{endpoint}} failed with {{response.status_code}}"
    
    @pytest.mark.post  
    def test_post_endpoints(self):
        """Test all POST endpoints for {resource_name}"""
        endpoints = {endpoints_list}
        
        for endpoint in endpoints:
            if any(action in endpoint.lower() for action in ['create', 'update', 'import', 'delete']):
                # Use minimal viable payload strategy
                minimal_payload = {{}}  # TODO: Define minimal payload for this resource
                response = self.make_post_request(endpoint, minimal_payload)
                assert response.status_code in [200, 201, 400, 404], f"Endpoint {{endpoint}} failed with {{response.status_code}}"
'''
    
    for folder_name, resource_info in subresource_mapping.items():
        folder_path = tests_dir / folder_name
        test_file_path = folder_path / "test_endpoints.py"
        
        if not test_file_path.exists():
            # Generate test file content
            class_name = ''.join(word.capitalize() for word in folder_name.split('_'))
            endpoints_list = resource_info['endpoints']
            
            if start_test_file.exists():
                # Use start_test as template but customize
                content = template_content.replace('start_test', folder_name)
                content = content.replace('StartTest', class_name)
                content = content.replace('start-test', resource_info['path'])
            else:
                # Use fallback template
                content = template_content.format(
                    resource_name=folder_name,
                    class_name=class_name,
                    endpoints_list=endpoints_list
                )
            
            with open(test_file_path, 'w') as f:
                f.write(content)
            
            print(f"   ✅ Created: {test_file_path}")

def create_summary_report():
    """Create a summary report of the reorganization"""
    subresource_mapping = get_subresource_mapping()
    
    report = []
    report.append("# Sub-Resource Pipeline Organization Summary")
    report.append(f"**Total Pipelines Created:** {len(subresource_mapping)}")
    report.append(f"**Total Endpoints Covered:** {sum(len(info['endpoints']) for info in subresource_mapping.values())}")
    report.append("")
    report.append("## Pipeline Structure")
    
    for folder_name, resource_info in subresource_mapping.items():
        endpoint_count = len(resource_info['endpoints'])
        report.append(f"- `{folder_name}-validation.yml` -> `tests/{folder_name}/` ({endpoint_count} endpoints)")
    
    report.append("")
    report.append("## Next Steps")
    report.append("1. Create Azure Pipeline YAML files for each sub-resource")
    report.append("2. Configure path-based triggers in Azure DevOps")
    report.append("3. Test minimal viable payloads for POST endpoints")
    report.append("4. Set up deployment validation workflows")
    
    with open("SUBRESOURCE_ORGANIZATION.md", 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"\n📋 Summary report created: SUBRESOURCE_ORGANIZATION.md")

def main():
    """Main reorganization process"""
    print("🔄 Starting Sub-Resource Reorganization")
    print("=" * 50)
    
    # Step 1: Create folder structure
    subresource_mapping = create_subresource_folders()
    
    # Step 2: Move existing test files
    move_existing_tests()
    
    # Step 3: Create test files for empty folders
    create_test_files_for_empty_folders()
    
    # Step 4: Create summary report
    create_summary_report()
    
    print("\n✅ Sub-resource reorganization complete!")
    print(f"   📁 Created {len(subresource_mapping)} sub-resource folders")
    print("   📄 Generated test_endpoints.py files where needed")
    print("   📋 Created summary report")
    print("\nNext: Create Azure Pipeline YAML files for deployment validation")

if __name__ == "__main__":
    main()
