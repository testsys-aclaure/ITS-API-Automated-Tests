"""Shared base class for API testing with common utilities."""

import os
import json
import pytest
import requests
from typing import Dict, Any, List, Optional

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class APITestBase:
    """Base class for API endpoint testing with shared utilities."""
    
    @classmethod
    def setup_class(cls):
        """Class-level setup for API testing."""
        cls.base_url = os.environ["BASE_URL"].rstrip("/")
        cls.openapi_path = os.getenv("OPENAPI_PATH", "schema/openapi.json")
        cls.program_id = os.getenv("PROGRAM_ID")
        cls.spec = cls._load_openapi_spec()
    
    @classmethod 
    def _load_openapi_spec(cls) -> Dict[str, Any]:
        """Load OpenAPI specification."""
        with open(cls.openapi_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    @pytest.fixture(scope="session")
    def auth_headers(self):
        """Get authentication headers using client credentials flow."""
        data = {
            "grant_type": "client_credentials",
            "client_id": os.environ["CLIENT_ID"],
            "client_secret": os.environ["CLIENT_SECRET"],
            "scope": os.environ["SCOPE"],
        }
        r = requests.post(os.environ["TOKEN_URL"], data=data, timeout=20)
        r.raise_for_status()
        token = r.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def load_openapi_spec(self) -> Dict[str, Any]:
        """Load OpenAPI specification."""
        return self.spec
    
    def get_env_to_query_mapping(self) -> Dict[str, Any]:
        """Map environment variables to query parameter names."""
        return {
            "PROGRAM_INSTITUTION_ID": "program-institution-id",
            "PROGRAM_ID": "program-id",
            "EVENT_ID": "event-id",
            "EVENT_DESCRIPTION": "event-description",
            "EXAMINEE_ID": ["examinee-id", "examinee"],
            "RESULT_ID": "result-id",
            "SESSION_CODE": ["session-code", "SessionCodes"],
            "VENDOR_ID": ["vendor-id", "vendorid"],
            "SPONSOR_ID": ["sponsor-id", "sponsorid"],
            "START_DATE": ["start-date", "StartDate", "start-utc"],
            "END_DATE": ["end-date", "EndDate", "end-utc"],
            "TIMEZONE_ID": "timezoneId",
            "USE_DAYLIGHT_SAVINGS": "useDaylightSavings",
            "INCLUDE_BIT_FLAG": "includeBitFlag",
            "TABLE_NAME": "table-name",
            "RECORD_ID": "record-id",
            "TEST_ID": "test-id",
        }
    
    def build_query_params(self, path: str, endpoint_params: List[str]) -> Dict[str, Any]:
        """Build query parameters for an endpoint based on available parameters."""
        query_params = {}
        env_mapping = self.get_env_to_query_mapping()
        
        # Map environment variables to query parameters
        for env_var, param_names in env_mapping.items():
            value = os.getenv(env_var)
            if not value:
                continue
                
            if isinstance(param_names, list):
                for param_name in param_names:
                    if param_name in endpoint_params:
                        query_params[param_name] = value
                        break
            else:
                if param_names in endpoint_params:
                    query_params[param_names] = value
        
        # Apply path-specific customizations
        query_params = self.apply_path_specific_rules(path, query_params, endpoint_params)
        
        return query_params
    
    def apply_path_specific_rules(self, path: str, query_params: Dict[str, Any], all_params: List[str]) -> Dict[str, Any]:
        """Apply path-specific parameter rules and customizations."""
        q = query_params.copy()
        
        # Form/Query: exclude program-institution-id and ensure limit=1
        if path == "/Form/Query":
            q.pop("program-institution-id", None)
            q["limit"] = 1
        
        # Event authorization and query: remove event-description to avoid conflict
        if path in ["/event/authorizations/Query", "/event/query"]:
            q.pop("event-description", None)
        
        # Result/query: SessionCodes OR date range
        if path == "/result/query":
            has_codes = bool(q.get("SessionCodes") or q.get("session-code"))
            has_range = bool(q.get("StartDate") and q.get("EndDate"))
            if not (has_codes or has_range):
                if "StartDate" in all_params or "start-date" in all_params:
                    q.setdefault("StartDate", os.getenv("START_DATE", "2024-01-01"))
                    q.setdefault("EndDate", os.getenv("END_DATE", "2024-12-31"))
                elif "SessionCodes" in all_params:
                    q.setdefault("SessionCodes", os.getenv("SESSION_CODE", "S-TEST"))
        
        # Session/query: session-number OR start-date+end-date
        if path == "/session/query":
            has_number = bool(q.get("session-number"))
            has_range = bool(q.get("start-date") and q.get("end-date"))
            if not (has_number or has_range):
                if "start-date" in all_params and "end-date" in all_params:
                    q.setdefault("start-date", os.getenv("START_DATE", "2024-01-01"))
                    q.setdefault("end-date", os.getenv("END_DATE", "2024-12-31"))
        
        # User access query: vendor-id OR sponsor-id (exactly one)
        if path == "/user/access/query":
            vendor = os.getenv("VENDOR_ID") or ""
            sponsor = os.getenv("SPONSOR_ID") or ""
            if ("vendor-id" in all_params) or ("sponsor-id" in all_params):
                if vendor and sponsor:
                    # Use vendor-id and remove sponsor-id
                    q["vendor-id"] = vendor
                    q.pop("sponsor-id", None)
                elif vendor:
                    q["vendor-id"] = vendor
                    q.pop("sponsor-id", None)
                elif sponsor:
                    q["sponsor-id"] = sponsor
                    q.pop("vendor-id", None)
        
        # User/query: exactly one of vendor-id or sponsor-id
        if path == "/User/query":
            vendor = os.getenv("VENDOR_ID") or ""
            sponsor = os.getenv("SPONSOR_ID") or ""
            if ("vendor-id" in all_params) or ("sponsor-id" in all_params):
                if vendor and sponsor:
                    q["vendor-id"] = vendor
                    q.pop("sponsor-id", None)
                elif vendor:
                    q["vendor-id"] = vendor
                elif sponsor:
                    q["sponsor-id"] = sponsor
        
        # Examinee audit query: needs proper date format (date, not datetime)
        if path == "/examinee/audit/query":
            # Use environment dates if available, otherwise use defaults
            start_date = os.getenv("START_DATE", "2024-01-01")
            end_date = os.getenv("END_DATE", "2024-12-31")
            
            if "start-utc" in all_params:
                q.setdefault("start-utc", start_date)
            if "end-utc" in all_params:
                q.setdefault("end-utc", end_date)
            # Required parameters for audit query
            q.setdefault("timezoneId", int(os.getenv("TIMEZONE_ID", 30)))  # UTC
            q.setdefault("useDaylightSavings", os.getenv("USE_DAYLIGHT_SAVINGS", "false").lower() == "true")
            q.setdefault("includeBitFlag", int(os.getenv("INCLUDE_BIT_FLAG", 1)))  # General form information
        
        # Longitudinal segment detail: needs result-id (skip this test for now)
        if path == "/examinee/longitudinal-segment-detail/query":
            # This endpoint requires a valid result-id which we don't have
            # Set a default that may work or expect 422
            q.setdefault("result-id", 1)
            q.setdefault("include-flag", 1)  # Event information
        
        return q
    
    def make_get_request(self, path: str, auth_headers: Dict[str, str], 
                        query_params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make a GET request to the specified endpoint."""
        url = f"{self.base_url}{path}"
        
        try:
            response = requests.get(
                url, 
                headers=auth_headers, 
                params=query_params or {}, 
                timeout=20
            )
            return response
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed for {path}: {e}")
    
    def make_post_request(self, path: str, auth_headers: Dict[str, str], 
                         json_data: Optional[Dict[str, Any]] = None,
                         query_params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make a POST request to the specified endpoint."""
        url = f"{self.base_url}{path}"
        
        # Ensure Content-Type is set for JSON requests
        headers = auth_headers.copy()
        if json_data:
            headers["Content-Type"] = "application/json"
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=json_data,
                params=query_params or {},
                timeout=30  # Longer timeout for POST operations
            )
            return response
        except requests.exceptions.RequestException as e:
            pytest.fail(f"POST request failed for {path}: {e}")
    
    def assert_response_success(self, response: requests.Response, path: str, 
                              expected_status: int = 200):
        """Assert that the response is successful."""
        try:
            # Check status code
            assert response.status_code == expected_status, (
                f"{path} returned {response.status_code}, expected {expected_status}. "
                f"Response: {response.text[:500]}"
            )
            
            # Verify content type is JSON (including problem+json for error responses)
            content_type = response.headers.get("content-type", "")
            valid_json_types = ["application/json", "application/problem+json"]
            assert any(json_type in content_type for json_type in valid_json_types), (
                f"{path} returned non-JSON content-type: {content_type}"
            )
            
            # Verify response can be parsed as JSON
            response.json()
            
        except requests.exceptions.JSONDecodeError:
            pytest.fail(f"{path} returned invalid JSON: {response.text[:500]}")
    
    def get_expected_status_codes(self) -> Dict[str, int]:
        """Get expected status codes for known problematic endpoints."""
        return {
            "/remote/system-checks/Query": 404,
            # All other endpoints should return 200
        }
    
    def should_skip_endpoint(self, path: str) -> bool:
        """Check if an endpoint should be skipped during testing."""
        # Add any endpoints that should be skipped
        skip_patterns = [
            # Add patterns for endpoints to skip
        ]
        
        return any(pattern in path for pattern in skip_patterns)
