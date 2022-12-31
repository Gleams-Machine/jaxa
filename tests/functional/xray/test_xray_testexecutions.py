"""
Functional Tests covering: XRay Test Executions
"""
import datetime
import uuid

import pytest
from decouple import config

pytestmark = [pytest.mark.functional]


TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")


def test__xray_testexecutions__create_test_execution(jaxa_client):
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

    test_id = response.get("createTest").get("test").get("issueId")
    print(f"Test created: {test_id}")

    response = jaxa_client.xray_gql.test_executions.create_test_execution(
        project_id=TEST_PROJECT_ID,
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        testenvs=["UAT"],
        test_ids=[test_id],
    )
    assert response.get("createTestExecution").get("testExecution").get("issueId")
    assert (
        response.get("createTestExecution").get("testExecution").get("jira").get("key")
    )


def test__xray_testexecutions__add_testexecutions_to_testplan(jaxa_client):
    """ """
    uniq = str(uuid.uuid4())[:8]

    response = jaxa_client.xray_gql.test_plan.create_test_plan(
        project_id=TEST_PROJECT_ID,
        summary=f"Task: {uniq} [{str(datetime.datetime.now())}]",
    )
    testplan_id = response.get("createTestPlan").get("testPlan").get("issueId")
    testplan_key = response.get("createTestPlan").get("testPlan").get("jira").get("key")

    print(f"Created TestPlan: {testplan_key}")

    response = jaxa_client.xray_gql.tests.create_cucumber_test(
        project_id=TEST_PROJECT_ID,
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        gherkin="""
    Given a test is described using the Gherkin language
    When that test is read
    Then it is supposed to be more readable!
            """,
    )

    test_id = response.get("createTest").get("test").get("issueId")
    print(f"Test created: {test_id}")

    response = jaxa_client.xray_gql.test_executions.create_test_execution(
        project_id=TEST_PROJECT_ID,
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        testenvs=["UAT"],
        test_ids=[test_id],
    )
    testexecution_id = (
        response.get("createTestExecution").get("testExecution").get("issueId")
    )

    response = jaxa_client.xray_gql.test_executions.add_testexecutions_to_testplan(
        testplan_id=testplan_id, testexecution_ids=[testexecution_id]
    )
    assert response.get("addTestExecutionsToTestPlan").get("addedTestExecutions") == [
        testexecution_id
    ]
