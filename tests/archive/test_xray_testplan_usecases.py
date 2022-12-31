"""
TestPlan Use Cases
"""

import datetime
import uuid
import pytest
from decouple import config


TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")


@pytest.mark.usecases
def test__xray_testplan__add_tests_to_testplan(jirasync_client):
    """
    UC6: Add Tests to TestPlan

    ```
    As an automated synchronisation process
    I want to add specific Tests to a TestPlan
    So that a TestPlan contains the required Tests
    ```

    """
    uniq = str(uuid.uuid4())[:8]

    # create new test plan
    testplan_name = f"TestPlan {uniq} [{str(datetime.datetime.now())}]"
    testplan = jirasync_client.gql.test_plan.create_test_plan(
        project_id=TEST_PROJECT_ID,
        summary=testplan_name
    )
    testplan_id = jirasync_client.gql.test_plan.get_issueid_from_createtestplan_result(result=testplan)

    # create new tests
    test_ids = []
    for iteration in range(2):
        test = jirasync_client.gql.tests.create_generic_test(
            project_id=TEST_PROJECT_ID,
            summary=f"[{iteration}] Test {uniq} [{str(datetime.datetime.now())}]",
            unstructured=""
        )
        test_ids.append(jirasync_client.gql.tests.get_issueid_from_createtest_result(result=test))

    # assign test to testplan
    jirasync_client.gql.test_plan.assign_tests_to_testplan(
        test_ids=test_ids,
        testplan_id=testplan_id
    )

    response = jirasync_client.gql.test_plan.get_testplan_from_id(testplan_id=testplan_id)
    test_jira_ids = jirasync_client.gql.test_plan.get_test_issueids_from_gettestplan_result(response=response)
    assert test_jira_ids == test_ids
    jirasync_client.gql.test_plan.summarise_testplan_tests(response=response)


@pytest.mark.usecases
def test__xray_testplan__add_testset_to_testplan(jirasync_client):
    """
    UC7: Add TestSet to TestPlan

    ```
    As an automated synchronisation process
    I want to add Tests from a specific TestSet to a TestPlan
    So that a TestPlan contains the required Tests
    ```
    """
    uniq = str(uuid.uuid4())[:8]

    testset = jirasync_client.gql.test_sets.create_empty_testset(
        project_key=TEST_PROJECT_ID,
        summary=f"TestSet {uniq} [{str(datetime.datetime.now())}]"
    )
    testset_id = jirasync_client.gql.test_sets.get_testsetid_from_createtestset_result(result=testset)

    # create some tests
    test_ids = []
    for x in range(4):
        test = jirasync_client.gql.tests.create_generic_test(
            project_id="QD",
            summary=f"[{x}] Test {uniq} [{str(datetime.datetime.now())}]",
            unstructured=""
        )
        test_ids.append(jirasync_client.gql.tests.get_issueid_from_createtest_result(result=test))
    else:
        # assign test to testset
        jirasync_client.gql.test_sets.add_tests_to_testset(
            testset_id=testset_id,
            test_ids=test_ids,
        )

    response = jirasync_client.gql.test_sets.get_tests_in_testset(testset_id=testset_id)
    tests_to_add = jirasync_client.gql.test_sets.get_test_issue_ids_from_gettestset_result(result=response)

    testplan = jirasync_client.gql.test_plan.create_test_plan_with_tests(
        project_id=TEST_PROJECT_ID,
        summary=f"TestPlan {uniq} [{str(datetime.datetime.now())}]",
        test_ids=tests_to_add
    )

    testplan_id = jirasync_client.gql.test_plan.get_issueid_from_createtestplan_result(result=testplan)
    response = jirasync_client.gql.test_plan.get_testplan_from_id(testplan_id=testplan_id)
    jirasync_client.gql.test_plan.summarise_testplan_tests(response=response)


@pytest.mark.usecases
def test__xray_testplan__create_executions_on_testplan(jirasync_client, xray_seeders):
    """
    UC8: Execute Tests in TestPlan

    ```
    As an automated synchronisation process
    I want to execute Tests in a TestPlan
    So that I can assign the status of a Test Execution
    ```

    """
    uniq = str(uuid.uuid4())[:8]

    testplan_id = xray_seeders.loaded_testplan(
        jirasync_client=jirasync_client,
        test_project_id=TEST_PROJECT_ID,
        test_count=4
    )
    testplan = jirasync_client.gql.test_plan.get_testplan_from_id(testplan_id=testplan_id)
    test_ids = jirasync_client.gql.test_plan.get_test_issueids_from_gettestplan_result(response=testplan)
    # Now we can execute
    testexecution_ids = []
    testrun_ids = []
    for test_id in test_ids:
        # create a test execution ticket
        testexecution = jirasync_client.gql.test_executions.create_test_execution(
            project_id=TEST_PROJECT_ID,
            summary=f"Executed {uniq}",
            testenvs=["DEV"],
            test_ids=[test_id]
        )
        testexecution_id = jirasync_client.gql.test_executions.get_issueid_from_createtestexecution_result(result=testexecution)
        testexecution_ids.append(testexecution_id)

        # Get test runs for test executions
        testrun = jirasync_client.gql.test_runs.get_test_runs(
            testissue_ids=[test_id],
            testExecIssueIds=[testexecution_id]
        )
        testrun_id = jirasync_client.gql.test_runs.get_testrunid_from_gettestruns_result(result=testrun)
        testrun_ids.append(testrun_id)

    # add test execution to test plan
    jirasync_client.gql.test_executions.add_testexecutions_to_testplan(
        testplan_id=testplan_id,
        testexecution_ids=testexecution_ids
    )

    for execution_status in [
        ("To Do", "To Do", "To Do", "To Do"),
        ("Executing", "To Do", "To Do", "To Do"),
        ("Executing", "Executing", "To Do", "To Do"),
        ("Executing", "Executing", "Executing", "To Do"),
        ("Executing", "Executing", "Executing", "Executing"),
        ("Passed", "Executing", "Executing", "Executing"),
        ("Passed", "Failed", "Executing", "Executing"),
        ("Passed", "Failed", "Passed", "Executing"),
        ("Passed", "Failed", "Passed", "Failed"),
    ]:
        for test_count in range(4):
             jirasync_client.gql.test_runs.update_testrun_status(
                testrun_id=testrun_ids[test_count],
                status=execution_status[test_count]
            )
        response = jirasync_client.gql.test_plan.get_testplan_from_id(testplan_id=testplan_id)
        jirasync_client.gql.test_plan.summarise_testplan_execution_runs(response=response)
