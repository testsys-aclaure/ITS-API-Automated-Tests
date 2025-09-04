#!/usr/bin/env python3
"""
HTML Report Generator for test_all_get_light.py Results Only
"""

import json
import datetime


def extract_endpoint(test_id):
    """Extract endpoint from test node ID"""
    if '::test_all_gets[' in test_id:
        parts = test_id.split('[')
        if len(parts) > 1:
            endpoint_part = parts[1].split('-')[0]
            return endpoint_part
    return "Unknown"


def extract_request_info(error_text):
    """Extract HTTP request details from error message"""
    if not error_text:
        return None, None, None
    
    # Look for patterns like "GET /endpoint -> 422"
    import re
    
    # Extract method and endpoint
    method_match = re.search(r'(GET|POST|PUT|DELETE|PATCH) ([^\s]+) -> (\d+)', error_text)
    if not method_match:
        return None, None, None
    
    method = method_match.group(1)
    endpoint = method_match.group(2)
    status_code = method_match.group(3)
    
    # Extract query parameters
    query_match = re.search(r'Query=({[^}]*})', error_text)
    query = query_match.group(1) if query_match else "{}"
    
    # Extract response body
    body_match = re.search(r'Body=(.+?)(?:\n|$)', error_text, re.DOTALL)
    body = body_match.group(1).strip() if body_match else ""
    
    return {
        'method': method,
        'endpoint': endpoint,
        'status_code': status_code,
        'query': query,
        'body': body[:500] + "..." if len(body) > 500 else body  # Limit body length
    }, query, body


def render_test_block(endpoint, tests):
    """Render an HTML block for an endpoint's tests"""
    passed = [t for t in tests if t.get('outcome') == 'passed']
    failed = [t for t in tests if t.get('outcome') == 'failed']
    skipped = [t for t in tests if t.get('outcome') == 'skipped']
    
    status = "PASSED" if not failed else "FAILED"
    status_class = "pass" if not failed else "fail"
    
    html = f"""
    <div class="endpoint-section">
        <h3 class="endpoint-title {status_class}">{endpoint} - {status}</h3>
        <div class="test-stats">
            <span class="stat pass">Passed: {len(passed)}</span>
            <span class="stat fail">Failed: {len(failed)}</span>
            <span class="stat skip">Skipped: {len(skipped)}</span>
        </div>
        
        <div class="test-details">
    """
    
    # Show passed tests (collapsed by default)
    if passed:
        html += f"""
            <details>
                <summary class="pass">✓ {len(passed)} Passed</summary>
                <ul class="test-list">
        """
        for test in passed:
            html += f'<li class="test pass">✓ {test["nodeid"].split("::")[-1].split("[")[0]}</li>'
        html += "</ul></details>"
    
    # Show skipped tests
    if skipped:
        html += f"""
            <details>
                <summary class="skip">⊘ {len(skipped)} Skipped</summary>
                <ul class="test-list">
        """
        for test in skipped:
            reason = "No reason provided"
            if 'longrepr' in test and test['longrepr']:
                if isinstance(test['longrepr'], tuple) and len(test['longrepr']) > 2:
                    reason = test['longrepr'][2]
                else:
                    reason = str(test['longrepr'])
            html += f'<li class="test skip">⊘ {test["nodeid"].split("::")[-1].split("[")[0]}<br><small>{reason}</small></li>'
        html += "</ul></details>"
    
    # Show failed tests (expanded by default)
    if failed:
        html += f"""
            <details open>
                <summary class="fail">✗ {len(failed)} Failed</summary>
                <ul class="test-list">
        """
        for test in failed:
            error_msg = "No error details available"
            
            # Try to get error info from different locations
            error_text = None
            if 'call' in test and test['call'] and 'crash' in test['call'] and test['call']['crash']:
                error_text = test['call']['crash'].get('message', '')
            elif 'longrepr' in test and test['longrepr']:
                error_text = str(test['longrepr'])
            
            if error_text:
                request_info, query, body = extract_request_info(error_text)
                
                if request_info:
                    error_msg = f"""
<div class="request-info">
    <strong>{request_info['method']} {request_info['endpoint']}</strong> → <span class="status-{request_info['status_code']}">{request_info['status_code']}</span>
    <div class="query-params"><strong>Query:</strong> {request_info['query']}</div>
    <div class="response-body"><strong>Response:</strong><br><code>{request_info['body']}</code></div>
</div>"""
                else:
                    error_msg = error_text[:300] + "..." if len(error_text) > 300 else error_text
            
            test_name = test["nodeid"].split("::")[-1].split("[")[0]
            html += f'<li class="test fail">✗ {test_name}<div class="error">{error_msg}</div></li>'
        html += "</ul></details>"
    
    html += """
        </div>
    </div>
    """
    
    return html


def main():
    # Always use the most recent test results
    report_file = 'reports/report.json'
    try:
        with open(report_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {report_file} not found. Run pytest first.")
        return
    
    # Count totals
    total_passed = 0
    total_failed = 0
    total_skipped = 0
    
    # Group tests by endpoint
    endpoint_tests = {}
    
    # Use tests structure which is more direct
    for test in data.get('tests', []):
        endpoint = extract_endpoint(test.get('nodeid', ''))
        
        if endpoint not in endpoint_tests:
            endpoint_tests[endpoint] = []
        
        endpoint_tests[endpoint].append(test)
        
        # Count totals
        outcome = test.get('outcome', 'unknown')
        if outcome == 'passed':
            total_passed += 1
        elif outcome == 'failed':
            total_failed += 1
        elif outcome == 'skipped':
            total_skipped += 1
    
    # Generate HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>API Test Report - test_all_get_light.py Only</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat {{ padding: 10px 15px; border-radius: 5px; font-weight: bold; color: white; }}
        .stat.pass {{ background-color: #27ae60; }}
        .stat.fail {{ background-color: #e74c3c; }}
        .stat.skip {{ background-color: #f39c12; }}
        .endpoint-section {{ background: white; margin: 15px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .endpoint-title {{ margin: 0 0 15px 0; padding: 10px; border-radius: 5px; }}
        .endpoint-title.pass {{ background-color: #d5f4e6; color: #27ae60; border-left: 4px solid #27ae60; }}
        .endpoint-title.fail {{ background-color: #fdf2f2; color: #e74c3c; border-left: 4px solid #e74c3c; }}
        .test-stats {{ margin: 10px 0; }}
        .test-list {{ list-style: none; padding: 0; }}
        .test {{ margin: 5px 0; padding: 8px; border-radius: 4px; }}
        .test.pass {{ background-color: #d5f4e6; }}
        .test.fail {{ background-color: #fdf2f2; }}
        .test.skip {{ background-color: #fff3cd; }}
        .error {{ background-color: #f8f9fa; padding: 10px; border-left: 3px solid #e74c3c; margin: 5px 0; font-size: 12px; overflow-x: auto; }}
        .request-info {{ font-family: monospace; font-size: 11px; }}
        .query-params {{ margin: 5px 0; color: #666; }}
        .response-body {{ margin: 5px 0; }}
        .response-body code {{ background: #f1f1f1; padding: 2px 4px; border-radius: 3px; font-size: 10px; }}
        .status-422 {{ color: #e67e22; }}
        .status-404 {{ color: #e74c3c; }}
        .status-500 {{ color: #c0392b; }}
        details {{ margin: 10px 0; }}
        summary {{ cursor: pointer; font-weight: bold; padding: 5px; }}
        summary.pass {{ color: #27ae60; }}
        summary.fail {{ color: #e74c3c; }}
        summary.skip {{ color: #f39c12; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>API Test Report - test_all_get_light.py Only</h1>
        <p>Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Test File: tests/test_all_get_light.py</p>
    </div>
    
    <div class="summary">
        <div class="stat pass">Passed: {total_passed}</div>
        <div class="stat fail">Failed: {total_failed}</div>
        <div class="stat skip">Skipped: {total_skipped}</div>
        <div class="stat" style="background-color: #34495e;">Total: {total_passed + total_failed + total_skipped}</div>
    </div>
    
    <div class="endpoints">
"""
    
    # Sort endpoints for consistent output
    for endpoint in sorted(endpoint_tests.keys()):
        tests = endpoint_tests[endpoint]
        html += render_test_block(endpoint, tests)
    
    html += """
    </div>
</body>
</html>
"""
    
    # Write the HTML report
    with open('reports/report.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML report generated: reports/report.html")
    print(f"Summary: {total_passed} passed, {total_failed} failed, {total_skipped} skipped")
    print(f"Total tests: {total_passed + total_failed + total_skipped}")


if __name__ == "__main__":
    main()
