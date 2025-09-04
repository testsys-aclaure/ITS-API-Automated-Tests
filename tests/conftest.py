# tests/conftest.py
import os, time, threading, requests, pytest
from dotenv import load_dotenv; load_dotenv()
load_dotenv()

_cache = {"tok": None, "exp": 0.0}
_lock = threading.Lock()

def _fetch_token() -> tuple[str, float]:
    url = os.environ["TOKEN_URL"]  # e.g., https://identity-qa.testsys.io/connect/token
    data = {
        "grant_type": "client_credentials",
        "client_id": os.environ["CLIENT_ID"],
        "client_secret": os.environ["CLIENT_SECRET"],
    }
    if scope := os.getenv("SCOPE"):
        data["scope"] = scope
    r = requests.post(url, data=data, timeout=20)
    if r.status_code >= 400:
        raise RuntimeError(f"Token request failed {r.status_code}: {r.text[:400]}")
    p = r.json()
    tok = p.get("access_token")
    if not tok:
        raise RuntimeError(f"No access_token in response: {p}")
    ttl = int(p.get("expires_in", 3600))
    exp = time.time() + max(300, ttl - 300)  # refresh ~5 min early
    return tok, exp

def _get_token() -> str:
    with _lock:
        now = time.time()
        if not _cache["tok"] or now >= _cache["exp"]:
            _cache["tok"], _cache["exp"] = _fetch_token()
        return _cache["tok"]  # type: ignore[return-value]

@pytest.fixture(scope="session")
def base_url() -> str:
    url = os.getenv("BASE_URL")
    if not url:
        raise RuntimeError("BASE_URL is not set")
    return url


@pytest.fixture(scope="session")
def auth_headers() -> dict:
    return {"Authorization": f"Bearer {_get_token()}"}
