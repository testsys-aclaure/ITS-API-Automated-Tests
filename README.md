# ITS API Automated Tests

## Overview

This project provides automated testing for the ITS API endpoints with comprehensive HTML reporting.

## Project Structure

```
ITS-API-Automated-Tests/
├── tests/           # Test files
├── scripts/         # Utility scripts
├── reports/         # Generated reports
├── schema/          # API schemas
└── run_tests.py     # Main entry point
```

See `ORGANIZATION.md` for detailed structure information.

## Quick Start

**Single command workflow:**

```bash
python scripts/run_tests.py
```

This will:
1. Run the `test_all_get_light.py` tests (41 endpoints)
2. Generate an HTML report from results
3. Offer to open the report in your browser

## Test Files

- `tests/test_all_get_light.py` - Lightweight API endpoint tests (recommended)
- `tests/test_all_get.py` - Full API endpoint tests 
- `tests/test_api.py` - Additional API tests
- `tests/test_smoke.py` - Smoke tests

## Manual Process

If you prefer manual control:

```bash
# Run tests directly
pytest tests/test_all_get_light.py

# Generate HTML report
python scripts/generate_report.py

# View report in browser
start reports/report.html
```

2. **Generate HTML Report:**
   ```bash
   python generate_html_report_light_only.py
   ```

3. **View Report:**
   - Open `reports/report_light_only.html` in browser

### For All Tests

1. **Run Tests:**
   ```bash
   pytest tests/test_all_get.py
   ```

2. **Generate HTML Report:**
   ```bash
   python generate_html_report.py
   ```

### Report Features

- **Color-coded status:** Green (passed), Red (failed), Blue (skipped)
- **HTTP request details:** Method, endpoint, query parameters
- **Response information:** Status codes, error messages
- **Summary statistics:** Pass/fail/skip counts

## Configuration

### Environment Variables (.env)

Key environment variables for API testing:
- `BASE_URL` - API base URL
- `PROGRAM_ID` - Program identifier
- `PROGRAM_INSTITUTION_ID` - Institution identifier
- Various test data parameters (see .env file)

### pytest Configuration (pytest.ini)

Configures automatic HTML and JSON report generation:
```ini
[tool:pytest]
addopts = --html=reports/report.html --json-report --json-report-file=reports/report.json
```

## Project Structure

```
├── tests/
│   ├── test_all_get_light.py     # Lightweight API tests
│   ├── test_all_get.py           # Full API tests
│   ├── test_api.py               # Additional tests
│   └── conftest.py               # Test configuration
├── reports/                      # Generated reports
├── schema/
│   └── openapi.json             # API schema
├── generate_html_report_light_only.py  # Light report generator
├── generate_html_report.py             # Full report generator
├── pytest.ini                          # pytest configuration
├── requirements.txt                     # Python dependencies
└── .env                                # Environment variables
```

## Current Test Status

As of latest run:
- **35 passed, 6 failed** (85% pass rate)
- Failed endpoints typically return 500 (server errors) or 422 (validation errors)

## Troubleshooting

### Report Shows Old Results

If HTML report shows outdated results:
1. Ensure you run pytest before generating reports
2. Check that `report.json` timestamp is recent
3. For light tests, copy `report.json` to `report_light_only.json`:
   ```bash
   cp reports/report.json reports/report_light_only.json
   ```

### Environment Issues

1. Activate virtual environment: `.venv/Scripts/activate` (Windows)
2. Install dependencies: `pip install -r requirements.txt`
3. Verify `.env` file contains required variables

## Development Notes

- Test framework uses parametrized testing for efficient endpoint coverage
- Custom environment variable mapping system (ENV_TO_QUERY)
- Endpoint-specific parameter rules in `_apply_endpoint_rules` function
- Request parameter override system (`req_q`) for OpenAPI spec discrepancies
