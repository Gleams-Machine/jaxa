"""
Functional Tests covering: XRay Authentication
"""
import os

import pytest

pytestmark = [pytest.mark.functional, pytest.mark.xray, pytest.mark.authentication]


def test__xray__authentication(jaxa_client):
    """ """

    response = jaxa_client.xray_rest.authenticate.get_auth_token(
        client_id=os.environ["JAXA_JIRA_CLIENT_ID"],
        client_secret=os.environ["JAXA_JIRA_CLIENT_SECRET"],
    )
    assert response.startswith("ey")
