#!/usr/bin/env python3
"""
Project Cleanup Script for ITS API Automated Tests
"""

import os
import glob
from pathlib import Path

def cleanup_debug_files():
    """Remove temporary debug files"""
    debug_files = [
        'debug.py',
        'debug2.py', 
        'debug3.py',
        'debug_test_count.py'
    ]
    
    removed_files = []
    for file in debug_files:
        if os.path.exists(file):
            print(f"Removing debug file: {file}")
            os.remove(file)
            removed_files.append(file)
    
    return removed_files

def cleanup_old_reports():
    """Clean up old report files, keeping only the most recent"""
    reports_dir = Path('reports')
    
    # Keep these essential files
    keep_files = {
        'report.html',
        'report.json', 
        'report_light_only.html',
        'report_light_only.json'
    }
    
    removed_files = []
    for file in reports_dir.glob('*'):
        if file.is_file() and file.name not in keep_files:
            print(f"Removing old report: {file.name}")
            file.unlink()
            removed_files.append(file.name)
    
    return removed_files

def cleanup_pycache():
    """Remove __pycache__ directories"""
    removed_dirs = []
    for pycache_dir in glob.glob('**/__pycache__', recursive=True):
        print(f"Removing cache directory: {pycache_dir}")
        import shutil
        shutil.rmtree(pycache_dir)
        removed_dirs.append(pycache_dir)
    
    return removed_dirs

def main():
    """Run project cleanup"""
    print("=== ITS API Test Project Cleanup ===\n")
    
    # Cleanup debug files
    print("1. Cleaning up debug files...")
    debug_files = cleanup_debug_files()
    if debug_files:
        print(f"   Removed: {', '.join(debug_files)}")
    else:
        print("   No debug files to remove")
    
    # Cleanup old reports (optional - uncomment if desired)
    # print("\n2. Cleaning up old reports...")
    # old_reports = cleanup_old_reports()
    # if old_reports:
    #     print(f"   Removed: {', '.join(old_reports)}")
    # else:
    #     print("   No old reports to remove")
    
    # Cleanup Python cache
    print("\n3. Cleaning up Python cache...")
    cache_dirs = cleanup_pycache()
    if cache_dirs:
        print(f"   Removed: {', '.join(cache_dirs)}")
    else:
        print("   No cache directories to remove")
    
    print("\n=== Cleanup Complete ===")
    print("\nRemaining project structure:")
    print("├── tests/")
    print("├── reports/") 
    print("├── schema/")
    print("├── generate_html_report_light_only.py")
    print("├── generate_html_report.py")
    print("├── pytest.ini")
    print("├── requirements.txt")
    print("├── README.md")
    print("└── .env")

if __name__ == "__main__":
    main()
