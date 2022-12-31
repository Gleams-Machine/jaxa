"""
Functional Tests covering: XRay Authentication
"""
import pytest
from decouple import config

pytestmark = [pytest.mark.functional]


def test__xray__authentication(jaxa_client):
    """ """

    response = jaxa_client.xray_rest.authenticate.get_auth_token(
        client_id=config("JAXA_JIRA_CLIENT_ID"),
        client_secret=config("JAXA_JIRA_CLIENT_SECRET"),
    )
    assert response.startswith("ey")
