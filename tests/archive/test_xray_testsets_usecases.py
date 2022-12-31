"""

"""
import datetime
import uuid

import pytest
from decouple import config

TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")


@pytest.mark.usecases
def test__xray_testsets__create_testset_with_tests(jirasync_client):
    """
    Use Case: UC3: Create TestSet with new Tests

    ```
    As an automated synchronisation process
    I want to create n automated tests in Xray and assign them to a new TestSet
    So that a TestSet is created containing the relevant tests
    ```

    """
    uniq = str(uuid.uuid4())[:8]

    # create some tests
    test_ids = []
    for x in range(4):
        test = jirasync_client.gql.tests.create_generic_test(
            project_id=TEST_PROJECT_ID,
            summary=f"[{x}] Test {uniq} [{str(datetime.datetime.now())}]",
            unstructured="",
        )
        test_ids.append(
            jirasync_client.gql.tests.get_issueid_from_createtest_result(test)
        )
    else:
        # assign test to testset
        response = jirasync_client.gql.test_sets.create_testset_with_tests(
            summary=f"TestSet {uniq} [{str(datetime.datetime.now())}]",
            test_ids=test_ids,
            project_key=TEST_PROJECT_ID,
        )
        testset_id = (
            jirasync_client.gql.test_sets.get_testsetid_from_createtestset_result(
                result=response
            )
        )

    # get summary of test set
    response = jirasync_client.gql.test_sets.get_tests_in_testset(testset_id=testset_id)
    jirasync_client.gql.test_sets.display_testset_tests(response=response)


@pytest.mark.usecases
def test__xray_testsets__add_tests_to_testset(jirasync_client):
    """
    UC4: Add Tests to TestSet

    ```
    As an automated synchronisation process
    I want to assign specific Tests to an existing TestSet
    So that a TestSet is updated to contain the relevant tests
    ```

    """
    uniq = str(uuid.uuid4())[:8]

    # create some tests
    test_ids = []
    for x in range(4):
        test = jirasync_client.gql.tests.create_generic_test(
            project_id=TEST_PROJECT_ID,
            summary=f"[{x}] Test {uniq} [{str(datetime.datetime.now())}]",
            unstructured="",
        )
        test_ids.append(
            jirasync_client.gql.tests.get_issueid_from_createtest_result(result=test)
        )
    else:
        # assign test to testset
        response = jirasync_client.gql.test_sets.create_testset_with_tests(
            summary=f"TestSet {uniq} [{str(datetime.datetime.now())}]",
            test_ids=test_ids,
            project_key=TEST_PROJECT_ID,
        )
        testset_id = (
            jirasync_client.gql.test_sets.get_testsetid_from_createtestset_result(
                result=response
            )
        )

    response = jirasync_client.gql.test_sets.get_tests_in_testset(testset_id=testset_id)
    tests_to_check = (
        jirasync_client.gql.test_sets.get_test_issue_ids_from_gettestset_result(
            result=response
        )
    )
    assert tests_to_check == test_ids

    added_tests = []
    for x in range(4):
        test = jirasync_client.gql.tests.create_generic_test(
            project_id="QD",
            summary=f"[{x}] Test {uniq} [{str(datetime.datetime.now())}]",
            unstructured="",
        )
        added_tests.append(
            jirasync_client.gql.tests.get_issueid_from_createtest_result(result=test)
        )

    # now add some new Tests
    jirasync_client.gql.test_sets.add_tests_to_testset(
        testset_id=testset_id, test_ids=added_tests
    )
    response = jirasync_client.gql.test_sets.get_tests_in_testset(testset_id=testset_id)
    tests_to_check = (
        jirasync_client.gql.test_sets.get_test_issue_ids_from_gettestset_result(
            result=response
        )
    )
    for added_test in added_tests:
        assert added_test in tests_to_check


@pytest.mark.usecases
def test__xray_testsets__remove_tests_from_testset(jirasync_client):
    """
    UC5: Remove Tests from TestSet

    ```
    As an automated synchronisation process
    I want to remove specific Tests from a TestSet
    So that a TestSet is updated to not contain the relevant tests
    ```
    """
    uniq = str(uuid.uuid4())[:8]

    # create some tests
    test_ids = []
    for x in range(4):
        test = jirasync_client.gql.tests.create_generic_test(
            project_id=TEST_PROJECT_ID,
            summary=f"[{x}] Test {uniq} [{str(datetime.datetime.now())}]",
            unstructured="",
        )
        test_ids.append(
            jirasync_client.gql.tests.get_issueid_from_createtest_result(result=test)
        )
    else:
        # assign test to testset
        response = jirasync_client.gql.test_sets.create_testset_with_tests(
            summary=f"TestSet {uniq} [{str(datetime.datetime.now())}]",
            test_ids=test_ids,
            project_key=TEST_PROJECT_ID,
        )
        testset_id = (
            jirasync_client.gql.test_sets.get_testsetid_from_createtestset_result(
                result=response
            )
        )

    response = jirasync_client.gql.test_sets.get_tests_in_testset(testset_id=testset_id)
    tests_to_check = (
        jirasync_client.gql.test_sets.get_test_issue_ids_from_gettestset_result(
            result=response
        )
    )
    assert tests_to_check == test_ids

    removed_tests = test_ids[::2]
    jirasync_client.gql.test_sets.remove_tests_from_testset(
        testset_id=testset_id, test_ids=removed_tests
    )
    response = jirasync_client.gql.test_sets.get_tests_in_testset(testset_id=testset_id)
    tests_to_check = [
        test.get("issueId", "")
        for test in response.get("getTestSet", {}).get("tests", {}).get("results", [])
    ]
    for removed_test in removed_tests:
        assert removed_test not in tests_to_check
