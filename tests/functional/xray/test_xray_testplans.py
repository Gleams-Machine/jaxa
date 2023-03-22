"""
Functional Tests covering: XRay Testplans
"""
import datetime
import os
import uuid

import pytest

pytestmark = [pytest.mark.functional, pytest.mark.testplans, pytest.mark.xray]


def test__xray_testplans__create_testplan(jaxa_client):
    """ """
    uniq = str(uuid.uuid4())[:8]
    response = jaxa_client.xray_gql.test_plan.create_test_plan(
        project_id=os.environ["JAXA_PROJECT_ID"],
        summary=f"Task: {uniq} [{str(datetime.datetime.now())}]",
    )
    assert response.get("createTestPlan").get("testPlan").get("issueId")
    assert response.get("createTestPlan").get("testPlan").get("jira").get("key")

    # response = jaxa_client.xray_gql.test_plan.get_testplan_from_id(
    #     testplan_id=response.get("createTestPlan").get("testPlan").get("issueId")
    # )
    # print(response)


def test__xray_testplans__create_test_plan_with_tests(jaxa_client):
    """ """
    uniq = str(uuid.uuid4())[:8]

    test_ids = []
    for _ in range(3):
        response = jaxa_client.xray_gql.tests.create_generic_test(
            project_id=os.environ["JAXA_PROJECT_ID"],
            summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
            unstructured="test steps",
        )
        test_ids.append(response.get("createTest").get("test").get("issueId"))

    response = jaxa_client.xray_gql.test_plan.create_test_plan_with_tests(
        project_id=os.environ["JAXA_PROJECT_ID"],
        summary=f"TestPlan: {uniq} [{str(datetime.datetime.now())}]",
        test_ids=test_ids,
    )
    testplan_id = response.get("createTestPlan").get("testPlan").get("issueId")
    testplan_key = response.get("createTestPlan").get("testPlan").get("jira").get("key")
    print(f"Created TestPlan: {testplan_key}")
    assert testplan_id
    assert testplan_key
