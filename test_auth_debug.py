#!/usr/bin/env python3
"""Debug which auth fixture is being used."""

import pytest
from tests.shared import APITestBase

class TestAuthDebug(APITestBase):
    def test_which_auth_fixture(self, auth_headers):
        """Test to see which auth_headers fixture is being used."""
        print(f"\nauth_headers type: {type(auth_headers)}")
        print(f"auth_headers value: {auth_headers}")
        print(f"Has Authorization key: {'Authorization' in auth_headers}")
        if 'Authorization' in auth_headers:
            token = auth_headers['Authorization']
            print(f"Token starts with Bearer: {token.startswith('Bearer ')}")
            print(f"Token length: {len(token)}")
        
        # This should pass if we have a valid token
        assert 'Authorization' in auth_headers
        assert auth_headers['Authorization'].startswith('Bearer ')
