"""
🏗️ Generate Azure Pipeline YAML Files
Creates all 43 pipeline validation files for sub-resource deployment strategy
"""

import os
from pathlib import Path

def get_subresource_mapping():
    """Returns the complete sub-resource mapping"""
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

def create_pipeline_yaml(resource_name, resource_info):
    """Create a pipeline YAML file for a specific resource"""
    
    # Convert resource name to display name
    display_name = ' '.join(word.capitalize() for word in resource_name.split('_'))
    
    # Create the pipeline content
    content = f"""trigger:
  branches:
    include:
    - main
    - develop
  paths:
    include:
    - tests/{resource_name}/**
    - tests/shared/**

pool:
  vmImage: 'ubuntu-latest'

variables:
  pythonVersion: '3.11'

jobs:
- job: {resource_name.title().replace('_', '')}Validation
  displayName: '{display_name} API Validation'
  
  steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '$(pythonVersion)'
    displayName: 'Use Python $(pythonVersion)'

  - script: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
    displayName: 'Install dependencies'

  - script: |
      pytest tests/{resource_name}/ -v --junitxml=test-results.xml
    displayName: 'Run {display_name} tests'
    env:
      API_BASE_URL: $(QA_API_BASE_URL)
      API_TOKEN: $(QA_API_TOKEN)

  - task: PublishTestResults@2
    condition: succeededOrFailed()
    inputs:
      testResultsFiles: 'test-results.xml'
      testRunTitle: '{display_name} API Tests'

  - script: |
      if [ $? -ne 0 ]; then
        echo "##vso[task.logissue type=error]{display_name} API validation failed - blocking deployment"
        exit 1
      fi
    displayName: 'Validate test results'
"""
    
    return content

def generate_all_pipelines():
    """Generate all 43 pipeline YAML files"""
    subresource_mapping = get_subresource_mapping()
    pipelines_dir = Path("pipelines")
    
    print("🏗️  Generating Azure Pipeline YAML files...")
    print("=" * 50)
    
    created_count = 0
    
    for resource_name, resource_info in subresource_mapping.items():
        pipeline_filename = f"{resource_name}-validation.yml"
        pipeline_path = pipelines_dir / pipeline_filename
        
        # Skip if file already exists (don't overwrite examples)
        if pipeline_path.exists():
            print(f"   ⏭️  Skipped (exists): {pipeline_path}")
            continue
        
        # Create the pipeline file
        content = create_pipeline_yaml(resource_name, resource_info)
        
        with open(pipeline_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        created_count += 1
        endpoint_count = len(resource_info['endpoints'])
        print(f"   ✅ Created: {pipeline_filename} ({endpoint_count} endpoints)")
    
    print("\n" + "=" * 50)
    print(f"✅ Generated {created_count} pipeline files")
    print(f"📁 Total pipeline files: {len(list(pipelines_dir.glob('*-validation.yml')))}")
    print("\n🔧 Next steps:")
    print("1. Configure Azure DevOps to use these pipeline files")
    print("2. Set up QA_API_BASE_URL and QA_API_TOKEN variables")
    print("3. Test path-based triggers for each sub-resource")

def main():
    """Main execution"""
    generate_all_pipelines()

if __name__ == "__main__":
    main()
