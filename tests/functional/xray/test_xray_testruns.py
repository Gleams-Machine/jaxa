"""
Functional Tests covering: XRay Test Runs
"""
import datetime
import os
import uuid
from pathlib import Path

import pytest

pytestmark = [pytest.mark.functional, pytest.mark.xray, pytest.mark.testruns]
THIS_DIR = Path(__file__).parent
FILES_DIR = THIS_DIR / Path("files")


def test__xray_testruns__get_test_runs(jaxa_client):
    """ """
    uniq = str(uuid.uuid4())[:8]

    response = jaxa_client.xray_gql.tests.create_cucumber_test(
        project_id=os.environ["JAXA_PROJECT_ID"],
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        gherkin="""
    Given a test is described using the Gherkin language
    When that test is read
    Then it is supposed to be more readable!
            """,
    )

    test_id = response.get("createTest").get("test").get("issueId")
    print(f"Test created: id={test_id}")

    response = jaxa_client.xray_gql.test_executions.create_test_execution(
        project_id=os.environ["JAXA_PROJECT_ID"],
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        testenvs=["UAT"],
        test_ids=[test_id],
    )
    testexecution_id = (
        response.get("createTestExecution").get("testExecution").get("issueId")
    )

    testrun = jaxa_client.xray_gql.test_runs.get_test_runs(
        testissue_ids=[test_id], testExecIssueIds=[testexecution_id]
    )
    testrun_id = testrun.get("getTestRuns").get("results")[0].get("id")
    print(f"Test Run created: id={testrun_id}")
    assert testrun_id


def test__xray_testruns__update_testrun_status(jaxa_client):
    """ """
    uniq = str(uuid.uuid4())[:8]

    response = jaxa_client.xray_gql.tests.create_cucumber_test(
        project_id=os.environ["JAXA_PROJECT_ID"],
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        gherkin="""
    Given a test is described using the Gherkin language
    When that test is read
    Then it is supposed to be more readable!
            """,
    )

    test_id = response.get("createTest").get("test").get("issueId")
    print(f"Test created: id={test_id}")

    response = jaxa_client.xray_gql.test_executions.create_test_execution(
        project_id=os.environ["JAXA_PROJECT_ID"],
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        testenvs=["UAT"],
        test_ids=[test_id],
    )
    testexecution_id = (
        response.get("createTestExecution").get("testExecution").get("issueId")
    )

    testrun = jaxa_client.xray_gql.test_runs.get_test_runs(
        testissue_ids=[test_id], testExecIssueIds=[testexecution_id]
    )
    testrun_id = testrun.get("getTestRuns").get("results")[0].get("id")
    print(f"Test Run created: id={testrun_id}")
    assert testrun_id

    update = jaxa_client.xray_gql.test_runs.update_testrun_status(
        testrun_id=testrun_id, status="Blocked"
    )
    assert update


def test__xray_testruns__add_testrun_evidence(jaxa_client):
    """ """
    uniq = str(uuid.uuid4())[:8]

    response = jaxa_client.xray_gql.tests.create_cucumber_test(
        project_id=os.environ["JAXA_PROJECT_ID"],
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        gherkin="""
    Given a test is described using the Gherkin language
    When that test is read
    Then it is supposed to be more readable!
            """,
    )

    test_id = response.get("createTest").get("test").get("issueId")
    print(f"Test created: id={test_id}")

    response = jaxa_client.xray_gql.test_executions.create_test_execution(
        project_id=os.environ["JAXA_PROJECT_ID"],
        summary=f"Test: {uniq} [{str(datetime.datetime.now())}]",
        testenvs=["UAT"],
        test_ids=[test_id],
    )
    testexecution_id = (
        response.get("createTestExecution").get("testExecution").get("issueId")
    )

    testrun = jaxa_client.xray_gql.test_runs.get_test_runs(
        testissue_ids=[test_id], testExecIssueIds=[testexecution_id]
    )
    testrun_id = testrun.get("getTestRuns").get("results")[0].get("id")
    print(f"Test Run created: id={testrun_id}")
    assert testrun_id

    evidence_file = FILES_DIR / "log_sample.json"
    update = jaxa_client.xray_gql.test_runs.add_testrun_evidence(
        testrun_id=testrun_id, filepath=evidence_file
    )
    assert update
