#!/usr/bin/env python3
"""
Simple Test Runner and Report Generator for ITS API Tests
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{description}...")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("✓ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def main():
    """Run tests and generate report"""
    print("🚀 ITS API Test Runner")
    print("=" * 30)
    
    # Determine which test file to run
    test_file = "tests/test_all_get_light.py"  # The file you've been working on
    
    # Check if virtual environment exists
    venv_prefix = ""
    if Path('.venv').exists():
        if os.name == 'nt':  # Windows
            venv_prefix = ".venv\\Scripts\\activate && "
        else:  # Unix/Linux/Mac
            venv_prefix = "source .venv/bin/activate && "
    
    # Run tests
    test_cmd = f"{venv_prefix}pytest {test_file} --json-report --json-report-file=reports/report.json"
    if not run_command(test_cmd, f"Running {test_file}"):
        return False
    
    # Generate HTML report
    report_cmd = f"{venv_prefix}python generate_report.py"
    if not run_command(report_cmd, "Generating HTML report"):
        return False
    
    print(f"\n🎉 Test run completed!")
    print("📊 Report available at: reports/report.html")
    
    # Ask if user wants to open report
    if input(f"\nOpen report in browser? (y/n): ").lower().startswith('y'):
        report_path = Path('reports/report.html').absolute()
        try:
            if os.name == 'nt':  # Windows
                os.startfile(report_path)
            else:  # Unix/Linux/Mac
                subprocess.run(['open', report_path])
            print(f"📖 Opened report in browser")
        except Exception as e:
            file_url = f"file:///{report_path.as_posix()}"
            print(f"Could not auto-open. Open manually: {file_url}")

if __name__ == "__main__":
    main()
