#!/usr/bin/env python3
"""
🔄 Rename Test Files to Be More Descriptive
Changes all test_endpoints.py files to test_[resource_name].py for better identification
"""

import os
import shutil
from pathlib import Path

def rename_test_files():
    """Rename all test_endpoints.py files to be more descriptive"""
    tests_dir = Path("tests")
    renamed_count = 0
    
    print("🔄 Renaming test files to be more descriptive...")
    print("=" * 60)
    
    # Find all test_endpoints.py files
    for test_file in tests_dir.glob("*/test_endpoints.py"):
        if test_file.parent.name == "shared":
            continue
            
        # Get the resource name from the folder
        resource_name = test_file.parent.name
        new_filename = f"test_{resource_name}.py"
        new_path = test_file.parent / new_filename
        
        # Rename the file
        test_file.rename(new_path)
        renamed_count += 1
        
        print(f"   ✅ {test_file} → {new_path}")
    
    print("\n" + "=" * 60)
    print(f"✅ Renamed {renamed_count} test files")
    print("\nNow each test file has a unique, descriptive name:")
    print("- tests/start_test/test_start_test.py")
    print("- tests/user/test_user.py") 
    print("- tests/examinee_events/test_examinee_events.py")
    print("- etc.")

def update_imports_if_needed():
    """Check if any files import test_endpoints and update them"""
    tests_dir = Path("tests")
    
    print("\n🔍 Checking for any imports that need updating...")
    
    # Search for any imports of test_endpoints
    for py_file in tests_dir.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "test_endpoints" in content and "import" in content:
                print(f"   ⚠️  Found reference in: {py_file}")
                # We'll just print these for now since we don't expect any
        except Exception:
            pass

def main():
    """Main execution"""
    rename_test_files()
    update_imports_if_needed()
    
    print("\n🎉 Test file renaming complete!")
    print("Now you can easily identify which test is which:")
    print("- Much clearer error messages")
    print("- Better IDE navigation") 
    print("- Easier debugging")

if __name__ == "__main__":
    main()
