import os, schemathesis

OPENAPI_PATH = os.getenv("OPENAPI_PATH", "schema/openapi.json")
BASE_URL = os.getenv("BASE_URL", "")

schema = schemathesis.from_path(OPENAPI_PATH).base_url(BASE_URL)

@schema.parametrize()
def test_api_contract(case, auth_headers):
    case.call_and_validate(headers=auth_headers)
