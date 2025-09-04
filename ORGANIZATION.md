# Project Organization

## File Structure
```
ITS-API-Automated-Tests/
├── .env                        # Environment variables and API credentials
├── .gitignore                  # Git ignore patterns
├── requirements.txt            # Python dependencies
├── pytest.ini                 # pytest configuration
├── README.md                   # Main project documentation
├── PROJECT_STATUS.md           # Current project status
├── 
├── tests/                      # Test files
│   ├── conftest.py            # pytest configuration
│   ├── test_all_get_light.py # Main test file (41 API endpoints) ⭐
│   ├── test_all_get.py        # Full test suite (legacy)
│   ├── test_api.py            # Additional API tests
│   └── test_smoke.py          # Smoke tests
├── 
├── schema/                     # API schemas
│   └── openapi.json          # OpenAPI specification
├── 
├── reports/                    # Generated test reports
│   ├── report.html            # Main HTML report ⭐
│   ├── report.json            # JSON test data
│   ├── junit.xml              # JUnit format (pytest default)
│   └── all-get.xml            # Additional XML output
├── 
├── scripts/                    # Utility scripts
│   ├── run_tests.py           # Main test runner ⭐
│   ├── generate_report.py     # HTML report generator ⭐
│   └── cleanup_project.py     # Project maintenance
└── 
└── azure-pipelines.yml        # CI/CD pipeline configuration
```

## Key Files ⭐

### Primary Workflow
- `run_tests.py` - One-command test execution
- `test_all_get_light.py` - Main test file you've been working on
- `generate_report.py` - Creates HTML reports from test results
- `reports/report.html` - Main output report

### Configuration
- `.env` - API credentials and test parameters
- `pytest.ini` - Test execution configuration
- `requirements.txt` - Python dependencies

### Documentation
- `README.md` - Usage instructions
- `PROJECT_STATUS.md` - Current status and next steps

## Daily Workflow
```bash
# Run tests and generate report
python run_tests.py

# View results
# Open reports/report.html in browser
```

## File Relationships
```
.env → test_all_get_light.py → reports/report.json → generate_report.py → reports/report.html
  ↑            ↑                       ↑                    ↑                    ↑
config    test execution          test data           report generation      final output
```
