"""
Functional Tests covering: XRay Tests
"""
import datetime
import uuid

import pytest
from decouple import config

pytestmark = [pytest.mark.functional]


TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")


def test__xray_tests__create_cucumber_test(jaxa_client):
    """ """
    uniq = str(uuid.uuid4())[:8]
    response = jaxa_client.xray_gql.tests.create_cucumber_test(
        project_id=TEST_PROJECT_ID,
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        gherkin="""
Given a test iis described using the Gherkin language
When that test is read
Then it is supposed to be more readable!
        """,
    )
    assert response.get("createTest").get("test").get("issueId")
    assert response.get("createTest").get("test").get("jira").get("key")
    assert (
        response.get("createTest").get("test").get("testType").get("name") == "Cucumber"
    )


def test__xray_tests__create_generic_test(jaxa_client):
    """ """
    uniq = str(uuid.uuid4())[:8]
    response = jaxa_client.xray_gql.tests.create_generic_test(
        project_id=TEST_PROJECT_ID,
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        unstructured="""
- Go here
- Click this
- type some data
- check result
        """,
    )
    assert response.get("createTest").get("test").get("issueId")
    assert response.get("createTest").get("test").get("jira").get("key")
    assert (
        response.get("createTest").get("test").get("testType").get("name") == "Generic"
    )


def test__xray_tests__create_manual_test(jaxa_client):
    """ """
    uniq = str(uuid.uuid4())[:8]
    response = jaxa_client.xray_gql.tests.create_manual_test(
        project_id=TEST_PROJECT_ID,
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        steps=[
            {"action": "Create first example step", "result": "First step was created"},
            {
                "action": "Create second example step with data",
                "data": "Data for the step",
                "result": "Second step was created with data",
            },
        ],
    )
    assert response.get("createTest").get("test").get("issueId")
    assert response.get("createTest").get("test").get("jira").get("key")
    assert (
        response.get("createTest").get("test").get("testType").get("name") == "Manual"
    )
