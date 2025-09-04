#!/usr/bin/env python3
"""
🏗️ Rename Pipeline Files for Azure DevOps
Converts validation pipeline files to proper Azure DevOps naming convention
"""

import os
import shutil
from pathlib import Path

def rename_pipeline_files():
    """Rename pipeline files to Azure DevOps convention"""
    pipelines_dir = Path("pipelines")
    azure_pipelines_dir = Path("azure-pipelines")
    
    print("🏗️  Renaming pipeline files for Azure DevOps...")
    print("=" * 60)
    
    # Get all validation yml files
    validation_files = list(pipelines_dir.glob("*-validation.yml"))
    
    copied_count = 0
    
    for validation_file in validation_files:
        if "template" in validation_file.name:
            continue
            
        # Convert name: examinee_events-validation.yml -> examinee-events-azure-pipelines.yml
        base_name = validation_file.stem.replace("-validation", "").replace("_", "-")
        new_name = f"{base_name}-azure-pipelines.yml"
        new_path = azure_pipelines_dir / new_name
        
        # Copy the file
        shutil.copy2(validation_file, new_path)
        copied_count += 1
        
        print(f"   ✅ {validation_file.name} → {new_name}")
    
    print("\n" + "=" * 60)
    print(f"✅ Created {copied_count} Azure pipeline files")
    print(f"📁 Location: azure-pipelines/ folder")
    print("\n🔧 Next steps:")
    print("1. In Azure DevOps, create a pipeline for each file")
    print("2. Point each pipeline to its specific YAML file")
    print("3. Configure triggers and variables")

def create_pipeline_index():
    """Create an index of all pipeline files"""
    azure_pipelines_dir = Path("azure-pipelines")
    pipeline_files = sorted(azure_pipelines_dir.glob("*-azure-pipelines.yml"))
    
    index_content = []
    index_content.append("# Azure DevOps Pipeline Files")
    index_content.append(f"**Total Pipeline Files:** {len(pipeline_files)}")
    index_content.append("")
    index_content.append("## Sub-Resource Validation Pipelines")
    index_content.append("")
    
    for pipeline_file in pipeline_files:
        resource_name = pipeline_file.stem.replace("-azure-pipelines", "")
        test_folder = resource_name.replace("-", "_")
        index_content.append(f"- **{resource_name}**: `{pipeline_file.name}`")
        index_content.append(f"  - Tests: `tests/{test_folder}/`")
        index_content.append(f"  - Triggers on: `tests/{test_folder}/**` changes")
        index_content.append("")
    
    index_content.append("## Azure DevOps Setup")
    index_content.append("1. In Azure DevOps → Pipelines → New Pipeline")
    index_content.append("2. Choose 'Azure Repos Git' → Select this repository")
    index_content.append("3. Choose 'Existing Azure Pipelines YAML file'")
    index_content.append("4. Select the specific pipeline file for each sub-resource")
    index_content.append("5. Configure variables: `QA_API_BASE_URL`, `QA_API_TOKEN`")
    
    with open("azure-pipelines/README.md", 'w', encoding='utf-8') as f:
        f.write('\n'.join(index_content))
    
    print(f"\n📋 Created pipeline index: azure-pipelines/README.md")

def main():
    """Main execution"""
    rename_pipeline_files()
    create_pipeline_index()

if __name__ == "__main__":
    main()
