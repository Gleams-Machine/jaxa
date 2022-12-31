"""
Functional Tests covering: Fields
"""
import datetime
import uuid

import pytest
from decouple import config

pytestmark = [pytest.mark.functional]


TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")


def test__jira_fields__(jaxa_client):
    """ """
    pass
