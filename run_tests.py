#!/usr/bin/env python3
"""
Main Test Runner for ITS API Tests
Simple entry point that runs test_all_get_light.py and generates HTML report
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Quick test runner"""
    print("🚀 Running ITS API Tests")
    print("=" * 30)
    
    # Ensure we're in the right directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if venv is activated
    if not os.environ.get('VIRTUAL_ENV'):
        print("⚠️  Virtual environment not activated!")
        print("Please run: .venv\\Scripts\\activate.bat")
        print("Then run: python run_tests.py")
        return 1
    
    # Run tests
    print("Running tests/test_all_get_light.py...")
    test_cmd = [sys.executable, "-m", "pytest", "tests/test_all_get_light.py", "-v"]
    
    try:
        result = subprocess.run(test_cmd, check=False)
        print(f"\nTests completed with exit code: {result.returncode}")
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1
    
    # Generate report
    print("\nGenerating HTML report...")
    report_script = project_root / "scripts" / "generate_report.py"
    
    if not report_script.exists():
        print(f"Error: {report_script} not found")
        return 1
    
    try:
        subprocess.run([sys.executable, str(report_script)], check=True)
        print("✓ Report generated successfully")
        
        # Ask if user wants to open report
        response = input("\nOpen report in browser? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            report_file = project_root / "reports" / "report.html"
            if report_file.exists():
                subprocess.run(f'start "" "{report_file}"', shell=True)
                print("Report opened in browser")
            else:
                print("Report file not found")
        
    except subprocess.CalledProcessError as e:
        print(f"Error generating report: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
