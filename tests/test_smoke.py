# tests/test_smoke.py
import os
import requests
import pytest

def _q(d):
    return {k: v for k, v in d.items() if v not in (None, "", [], {})}

@pytest.fixture(scope="session")
def _cfg():
    base = os.getenv("BASE_URL")
    program_id = os.getenv("PROGRAM_ID")
    assert base, "BASE_URL is not set"
    assert program_id, "PROGRAM_ID is not set"
    return {"BASE": base.rstrip("/"), "PROGRAM_ID": int(program_id)}

def test_examinee_query(auth_headers, _cfg):
    params = _q({"program-id": _cfg["PROGRAM_ID"], "limit": 1})
    r = requests.get(f"{_cfg['BASE']}/examinee/query", headers=auth_headers, params=params, timeout=30)
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_event_query(auth_headers, _cfg):
    params = _q({"program-id": _cfg["PROGRAM_ID"], "limit": 1})
    r = requests.get(f"{_cfg['BASE']}/event/query", headers=auth_headers, params=params, timeout=30)
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_result_query(auth_headers, _cfg):
    params = _q({"program-id": _cfg["PROGRAM_ID"], "limit": 1})
    r = requests.get(f"{_cfg['BASE']}/result/query", headers=auth_headers, params=params, timeout=30)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
