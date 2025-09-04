#!/usr/bin/env python3
"""
🔧 Fix Import Statements in Generated Test Files
Updates all test files to use correct import for APITestBase
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix import statements in a single test file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the incorrect import
        old_import = "from tests.shared import APITestBase"
        new_import = "from tests.shared.api_test_base import APITestBase"
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
    except Exception as e:
        print(f"   ❌ Error fixing {file_path}: {e}")
        return False
    
    return False

def fix_all_imports():
    """Fix import statements in all test files"""
    tests_dir = Path("tests")
    fixed_count = 0
    
    print("🔧 Fixing import statements in test files...")
    print("=" * 50)
    
    # Find all test_endpoints.py files
    for test_file in tests_dir.glob("*/test_endpoints.py"):
        if fix_imports_in_file(test_file):
            print(f"   ✅ Fixed: {test_file}")
            fixed_count += 1
        else:
            print(f"   ⏭️  Skipped: {test_file}")
    
    print("\n" + "=" * 50)
    print(f"✅ Fixed imports in {fixed_count} files")

def main():
    """Main execution"""
    fix_all_imports()

if __name__ == "__main__":
    main()
