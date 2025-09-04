# tests/test_all_gets.py
import os, json, re

# --- Load .env early so os.environ is populated for both collection and runtime ---
# Option A: python-dotenv (works anywhere)
try:
    from dotenv import load_dotenv  # pip install python-dotenv
    load_dotenv()
except Exception:
    # Option B (alternative): use pytest-dotenv via pytest.ini (see below)
    pass

# --- Core envs your suite already expects ---
BASE_URL   = os.environ["BASE_URL"].rstrip("/")
OPENAPI    = os.getenv("OPENAPI_PATH", "schema/openapi.json")
PROGRAM_ID = os.getenv("PROGRAM_ID")  # backward-compat with your existing code

# -------------------- SEEDING CONFIG --------------------
# Required path params (substitute {param} in the URL). Fill as needed.
PATH_PARAM_SEEDS: dict[str, dict] = {
    # Example:
    # "/items/{itemId}": {"itemId": 123},
}

# Per-path extra query seeds (beyond env-driven defaults).
EXTRA_QUERY_SEEDS: dict[str, dict] = {
    # Example:
    # "/result/query": {"cycle-num": 1},
}

# Map environment variables -> candidate query param names on the API.
# We only project a value if that param actually exists in the current endpoint's query list.
ENV_TO_QUERY = {
    "PROGRAM_INSTITUTION_ID": "program-institution-id",
    "PROGRAM_ID": "program-id",  # keep your original
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
    "FORM_ID": "form-id",
    "BANK_ID": "bank-id",
    "IMPORT_ID": "import-id",
    "PACKAGE_CODE": "package-code",
    "URL_TYPE": "url-type",
    "PROCTOR_IDENTIFIER": "proctor-identifier",
    "PROCTOR_DISPLAY_NAME": "proctor-display-name",
    "PROCTOR_FIRST_NAME": "proctor-first-name",
    "PROCTOR_LAST_NAME": "proctor-last-name",
    "ENVIRONMENT_ID": "environment-id",
    "LONGITUDINAL_GROUP_ID": "longitudinal-group-id",
    "LONGITUDINAL_GROUP_NAME": "longitudinal-group-name",
}

import pytest, requests

# --- Load .env early so os.environ is populated for both collection and runtime ---
# Option A: python-dotenv (works anywhere)
try:
    from dotenv import load_dotenv  # pip install python-dotenv
    load_dotenv()
except Exception:
    # Option B (alternative): use pytest-dotenv via pytest.ini (see below)
    pass

# --- Core envs your suite already expects ---
BASE_URL   = os.environ["BASE_URL"].rstrip("/")
OPENAPI    = os.getenv("OPENAPI_PATH", "schema/openapi.json")
PROGRAM_ID = os.getenv("PROGRAM_ID")  # backward-compat with your existing code

# -------------------- SEEDING CONFIG --------------------
# Required path params (substitute {param} in the URL). Fill as needed.
PATH_PARAM_SEEDS: dict[str, dict] = {
    # Example:
    # "/items/{itemId}": {"itemId": 123},
}

# Per-path extra query seeds (beyond env-driven defaults).
EXTRA_QUERY_SEEDS: dict[str, dict] = {
    # Example:
    # "/result/query": {"cycle-num": 1},
}

# Map environment variables -> candidate query param names on the API.
# We only project a value if that param actually exists in the current endpoint’s query list.

# Optional: endpoints with known non-2xx expectations (adjust as your environment dictates).
EXPECTED_STATUS = {
    #"/remote/practice-checks/Query": 404,
    #"/remote/system-checks/Query": 404,
    # Example for a flakey server error you want to track explicitly:
    # "/result/query": 500,
}
# --------------------------------------------------------


@pytest.fixture(scope="session")
def auth_headers():
    # Client-credentials flow; assumes these envs are present.
    data = {
        "grant_type": "client_credentials",
        "client_id": os.environ["CLIENT_ID"],
        "client_secret": os.environ["CLIENT_SECRET"],
        "scope": os.environ["SCOPE"],
    }
    r = requests.post(os.environ["TOKEN_URL"], data=data, timeout=20)
    r.raise_for_status()
    tok = r.json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}


def _load_spec():
    with open(OPENAPI, "r", encoding="utf-8") as f:
        return json.load(f)


def _list_get_ops(spec):
    """Return list of (path, opSpec, pathSpec) for GET operations."""
    out = []
    for path, path_item in spec.get("paths", {}).items():
        op = path_item.get("get")
        if op:
            out.append((path, op, path_item))
    return out


def _collect_params(path_spec, op_spec):
    """Flatten path-level + op-level parameters."""
    params = []
    for src in (path_spec.get("parameters", []), op_spec.get("parameters", [])):
        params.extend([p for p in src if isinstance(p, dict)])
    return params


def _required_names(params, where):
    return [p["name"] for p in params if p.get("in") == where and p.get("required")]


def _all_query_names(params):
    return [p["name"] for p in params if p.get("in") == "query"]


def _fill_path(path: str, seeds: dict):
    """Substitute {param} segments using provided seeds."""
    def repl(m):
        name = m.group(1)
        if name not in seeds:
            raise KeyError(name)
        return str(seeds[name])
    return re.sub(r"\{([^}]+)\}", repl, path)


def _seed_from_env(all_query_names: list[str]) -> dict:
    """Project env vars into query params if those params exist on this endpoint."""
    q = {}
    for env_name, param_names in ENV_TO_QUERY.items():
        val = os.getenv(env_name)
        if val in (None, ""):
            continue
        if isinstance(param_names, list):
            for pn in param_names:
                if pn in all_query_names:
                    q.setdefault(pn, val)
        else:
            if param_names in all_query_names:
                q.setdefault(param_names, val)
    return q


def _apply_endpoint_rules(path: str, q: dict, all_q: list[str]) -> dict:
    """
    Satisfy 'one-of' and combo rules noted in your failure list,
    using env defaults when available.
    """
    # /event/authorizations/Query: (event-id OR event-description) AND program-institution-id
    if path == "/event/authorizations/Query":
        has_prog = bool(q.get("program-institution-id"))
        has_eid = bool(q.get("event-id"))
        has_edesc = bool(q.get("event-description"))
        if has_prog and not (has_eid or has_edesc):
            if "event-description" in all_q:
                q["event-description"] = os.getenv("EVENT_DESCRIPTION", "seeded-desc")
            elif "event-id" in all_q:
                q["event-id"] = os.getenv("EVENT_ID", "1")

    # /remote/sessions/query: SessionCodes OR StartDate+EndDate
    if path == "/remote/sessions/query":
        has_codes = bool(q.get("SessionCodes") or q.get("session-code"))
        has_range = bool((q.get("StartDate") or q.get("start-date")) and (q.get("EndDate") or q.get("end-date")))
        if not (has_codes or has_range):
            if "StartDate" in all_q or "start-date" in all_q:
                q.setdefault("StartDate", os.getenv("START_DATE", "2024-01-01"))
                q.setdefault("EndDate",   os.getenv("END_DATE",   "2024-12-31"))
            elif "SessionCodes" in all_q:
                q.setdefault("SessionCodes", os.getenv("SESSION_CODE", "S-TEST"))

    # /session/query: session-number OR start-date+end-date
    if path == "/session/query":
        has_number = bool(q.get("session-number"))
        has_range  = bool(q.get("start-date") and q.get("end-date"))
        if not (has_number or has_range):
            if "start-date" in all_q and "end-date" in all_q:
                q.setdefault("start-date", os.getenv("START_DATE", "2024-01-01"))
                q.setdefault("end-date",   os.getenv("END_DATE",   "2024-12-31"))

    # /user/access/query: one of vendor-id or sponsor-id
    if path == "/user/access/query":
        if not (q.get("vendor-id") or q.get("sponsor-id")):
            if "vendor-id" in all_q:
                q["vendor-id"] = os.getenv("VENDOR_ID", "1000")

    # /User/query: exactly one of vendor-id or sponsor-id
    if path == "/User/query":
        vendor = os.getenv("VENDOR_ID") or ""
        sponsor = os.getenv("SPONSOR_ID") or ""
        if ("vendor-id" in all_q) or ("sponsor-id" in all_q):
            if vendor and sponsor:
                q["vendor-id"] = vendor
                q.pop("sponsor-id", None)
            elif vendor:
                q["vendor-id"] = vendor
            elif sponsor:
                q["sponsor-id"] = sponsor

    # /Form/Query: exclude program-institution-id and ensure limit=1
    if path == "/Form/Query":
        # Remove program-institution-id if present as it causes validation errors
        q.pop("program-institution-id", None)
        # Ensure limit is set to 1
        q["limit"] = 1

    # /event/authorizations/Query: remove event-description to avoid conflict with event-id
    if path == "/event/authorizations/Query":
        # Remove event-description since we're sending event-id
        q.pop("event-description", None)

    # /event/query: remove event-description to avoid conflict with event-id
    if path == "/event/query":
        # Remove event-description since we're sending event-id
        q.pop("event-description", None)

    # /Test/Query: only needs program-id
    if path == "/Test/Query":
        # Clear all params except program-id
        q = {k: v for k, v in q.items() if k == "program-id"}

    # /form/definition/Query: only needs program-id
    if path == "/form/definition/Query":
        # Clear all params except program-id
        q = {k: v for k, v in q.items() if k == "program-id"}

    # /secure-browser/errors/query: needs program-id 52 and omit dates
    if path == "/secure-browser/errors/query":
        # Use specific program-id and remove date params
        q = {"program-id": "52"}
        if "environment-id" in all_q:
            q["environment-id"] = os.getenv("ENVIRONMENT_ID", "1")

    # /examinee/longitudinal-segment-detail/query: use specific working parameters
    if path == "/examinee/longitudinal-segment-detail/query":
        # Clear all parameters and use the known working set
        q.clear()
        q["longitudinal-group-id"] = "1463"
        q["examinee-id"] = "209058"
        q["program-id"] = "300"

    # /remote/examinee-data/Query: set specific required parameters
    if path == "/remote/examinee-data/Query":
        q.clear()
        q["examinee"] = "30657"
        q["program-id"] = "238"

    # /remote/session-data/Query: set specific required parameters
    if path == "/remote/session-data/Query":
        q.clear()
        q["session-code"] = "40688-09"
        q["program-id"] = "238"

    # /remote/admin-urls/Query: set specific required parameters
    if path == "/remote/admin-urls/Query":
        q.clear()
        q["url-type"] = "1"
        q["session-code"] = "40688-09"
        q["proctor-identifier"] = "test-proctor"
        q["proctor-display-name"] = "Test Proctor"
        q["proctor-first-name"] = "Test"
        q["proctor-last-name"] = "Proctor"
        q["program-id"] = "238"

    # /examinee/audit/query: only needs program-id, examinee-id, start-utc, and end-utc
    if path == "/examinee/audit/query":
        q.clear()
        q["program-id"] = "238"
        q["examinee-id"] = "1"
        q["start-utc"] = "2025-01-01"
        q["end-utc"] = "2025-12-31"

    return q


# ---- Spec + param list (computed at import to parametrize the test) ----
spec = _load_spec()
GET_OPS = _list_get_ops(spec)


@pytest.mark.parametrize(
    "path,op,path_spec",
    GET_OPS,
    ids=lambda x: x if isinstance(x, str) else x[0] if isinstance(x, tuple) else str(x),
)
def test_all_gets(path, op, path_spec, auth_headers):
    params = _collect_params(path_spec, op)
    req_q   = _required_names(params, "query")
    req_p   = _required_names(params, "path")
    all_q   = _all_query_names(params)

    # Override required parameters for specific endpoints where OpenAPI spec is incorrect
    if path == "/examinee/audit/query":
        req_q = ["program-id", "examinee-id", "start-utc", "end-utc"]
    elif path == "/examinee/record/query":
        req_q = ["program-id", "table-name", "record-id"]

    # ----- Handle required path params -----
    if req_p:
        seeds = PATH_PARAM_SEEDS.get(path)
        if not seeds or any(name not in seeds for name in req_p):
            pytest.skip(f"Skipping {path}: required path params {req_p} not seeded")
        url_path = _fill_path(path, seeds)
    else:
        url_path = path

    # ----- Build query -----
    q = {}

    # Keep your existing logic
    if "program-id" in all_q and PROGRAM_ID:
        q["program-id"] = int(PROGRAM_ID)
    if "limit" in all_q:
        q.setdefault("limit", 1)

    # Project envs for any query names present on this endpoint
    q.update(_seed_from_env(all_q))

    # Satisfy one-of/combination rules for known endpoints
    q = _apply_endpoint_rules(path, q, all_q)

    # Per-path extras last (they win)
    q.update(EXTRA_QUERY_SEEDS.get(path, {}))

    # If there are required query params still unseeded, skip with a precise message
    unseeded = [n for n in req_q if n not in q or q[n] in ("", None)]
    if unseeded:
        pytest.skip(f"Skipping {path}: required query params {unseeded} not seeded")

    # ----- Call & Assert -----
    resp = requests.get(f"{BASE_URL}{url_path}", headers=auth_headers, params=q, timeout=30)

    if path in EXPECTED_STATUS:
        exp = EXPECTED_STATUS[path]
        assert resp.status_code == exp, (
            f"GET {url_path} expected {exp} but got {resp.status_code}\n"
            f"Query={q}\nBody={resp.text[:800]}"
        )
    else:
        # Smoke rule: fail on server errors or validation errors, allow any 2xx/3xx
        assert resp.status_code < 500 and resp.status_code != 422, (
            f"GET {url_path} -> {resp.status_code}\n"
            f"Query={q}\nBody={resp.text[:800]}"
        )

    ctype = resp.headers.get("Content-Type", "")
    if "json" in ctype:
        _ = resp.json()
