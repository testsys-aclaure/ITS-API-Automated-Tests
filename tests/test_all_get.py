# tests/test_all_get.py  (v4-compatible)
import os, json
import schemathesis as st

OPENAPI_PATH = os.getenv("OPENAPI_PATH", "schema/openapi.json")
BASE_URL     = os.environ["BASE_URL"]
PROGRAM_ID   = os.getenv("PROGRAM_ID")

# Load the raw spec to inspect required / allowed params
with open(OPENAPI_PATH, "r", encoding="utf-8") as f:
    RAW_SPEC = json.load(f)

# v4: loaders live under schemathesis.openapi
schema = st.openapi.from_path(OPENAPI_PATH)
schema_get = schema.include(method="GET")  # v4: filter first, then parametrize

def _op_params(case):
    """Return (all_query_names, required_path_names) for this operation."""
    path_item = RAW_SPEC["paths"].get(case.path, {})
    op_spec = path_item.get(case.method.lower(), {})
    params = [p for p in (path_item.get("parameters", []) + op_spec.get("parameters", [])) if isinstance(p, dict)]
    all_q = [p["name"] for p in params if p.get("in") == "query"]
    req_path = [p["name"] for p in params if p.get("in") == "path" and p.get("required")]
    return all_q, req_path

# If you already have a token helper in conftest.py, you can import it:
# from tests.conftest import _get_token
# Otherwise do a simple env-based bearer header:
def _auth_header():
    token = os.getenv("BEARER_TOKEN")  # or replace with your _get_token() helper
    return {"Authorization": f"Bearer {token}"} if token else {}

@schema_get.parametrize()  # v4: no arguments here; filtering is done above
def test_every_get_operation(case):
    # Auth
    case.headers = {**(case.headers or {}), **_auth_header()}

    # Seed only if the param exists in this operation
    all_q, req_path = _op_params(case)

    if "program-id" in all_q and PROGRAM_ID:
        case.query = {**(case.query or {}), "program-id": int(PROGRAM_ID)}
    if "limit" in all_q:
        case.query = {**(case.query or {}), "limit": (case.query or {}).get("limit", 1)}

    # Skip endpoints with required path params we haven’t seeded
    if req_path:
        import pytest
        pytest.skip(f"Skipping {case.method} {case.path} (required path params: {req_path})")

    # Call & validate
    resp = case.call(base_url=BASE_URL, timeout=30)
    case.validate_response(resp)
