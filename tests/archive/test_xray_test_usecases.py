"""
Test Use Cases
"""

import datetime
import uuid
import pytest
from decouple import config


TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")
SAMPLE_GHERKIN = """
Given I want to create a test
When I call the correct API
Then a test is created
"""


@pytest.mark.usecases
def test__xray_test__create_generic_tests(jirasync_client):
    """
    Use Case: UC1: Create n generic tests

    Steps:
    - [Setup]
        - Create an empty TestPlan
    - [Assignment]
        - Create a few tests and assign each to TestPlan individually
    - [Verification]
        - Check tests are included on TestPlan
    """
    uniq = str(uuid.uuid4())[:8]
    test_count = 5

    for iteration in range(test_count):
        test = jirasync_client.gql.tests.create_generic_test(
            project_id=TEST_PROJECT_ID,
            summary=f"[{iteration}] Test {uniq} [{str(datetime.datetime.now())}]",
            unstructured=""
        )
        assert test.get("createTest", {}).get("warnings") == []
        assert test.get("createTest", {}).get("test", {}).get("testType", {}).get("name") == "Generic"
        assert test.get("createTest", {}).get("test", {}).get("issueId")
        assert test.get("createTest", {}).get("test", {}).get("jira", {}).get("key")


@pytest.mark.usecases
def test__xray_test__create_cucumber_tests(jirasync_client):
    """
    Use Case: UC2: Create n cucumber tests

    Steps:
    - [Setup]
        - Create an empty TestPlan
    - [Assignment]
        - Create a few tests and assign each to TestPlan individually
    - [Verification]
        - Check tests are included on TestPlan
    """
    uniq = str(uuid.uuid4())[:8]
    test_count = 5

    for iteration in range(test_count):
        test = jirasync_client.gql.tests.create_cucumber_test(
            project_id=TEST_PROJECT_ID,
            summary=f"[{iteration}] Test {uniq} [{str(datetime.datetime.now())}]",
            gherkin=SAMPLE_GHERKIN
        )
        assert test.get("createTest", {}).get("warnings") == []
        assert test.get("createTest", {}).get("test", {}).get("testType", {}).get("name") == "Cucumber"
        assert test.get("createTest", {}).get("test", {}).get("issueId")
        assert test.get("createTest", {}).get("test", {}).get("jira", {}).get("key")
