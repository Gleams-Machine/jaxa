import datetime
import uuid

from behave import *
from decouple import config

from features.steps.support import TestSetActions


@when("we opt to create an empty TestSet")
def step_impl(context):
    uniq = str(uuid.uuid4())[:8]
    summary = f"TestSet: {uniq} [{str(datetime.datetime.now())}]"

    context.execute_steps(
        f"when we opt to create an empty TestSet with summary {summary}"
    )


@then("a TestSet contains no tests")
def step_impl(context):
    response = TestSetActions.get_tests_in_testset(
        jaxa_client=context.jaxa.jaxa_client, testset_id=context.jaxa.active_testset_id
    )
    tests = response.get("getTestSet").get("tests").get("results")
    assert tests == []


@when("we opt to create an empty TestSet with summary {summary}")
def step_impl(context, summary):
    project_id = config("JAXA_TEST_PROJECT_ID")

    if "{uid}" in summary:
        summary = summary.replace("{uid}", str(uuid.uuid4())[:8])

    response = TestSetActions.create_empty_testset(
        jaxa_client=context.jaxa.jaxa_client, summary=summary, project_key=project_id
    )
    testset_id = response.get("createTestSet").get("testSet").get("issueId")
    testset_key = response.get("createTestSet").get("testSet").get("jira").get("key")
    context.jaxa.record_testset(
        testset_id=testset_id, testset_key=testset_key, summary=summary
    )


@when("we opt to create a TestSet with tests")
def step_impl(context):
    for row in context.table:
        test_type = row["test_type"]
        test_summary = row["test_summary"]
        context.execute_steps(
            "when we opt to create a {test_type} Test with summary {test_summary}".format(
                test_type=test_type, test_summary=test_summary
            )
        )

    uniq = str(uuid.uuid4())[:8]
    project_id = config("JAXA_TEST_PROJECT_ID")
    summary = f"TestSet: {uniq} [{str(datetime.datetime.now())}]"
    test_ids = list(context.jaxa.tests.keys())

    response = TestSetActions.create_testset_with_tests(
        jaxa_client=context.jaxa.jaxa_client,
        summary=summary,
        project_key=project_id,
        test_ids=test_ids,
    )
    testset_id = response.get("createTestSet").get("testSet").get("issueId")
    testset_key = response.get("createTestSet").get("testSet").get("jira").get("key")
    context.jaxa.record_testset(
        testset_id=testset_id, testset_key=testset_key, summary=summary
    )


@when("add a Test into the TestSet")
def step_impl(context):
    for row in context.table:
        test_type = row["test_type"]
        context.execute_steps(
            "when we opt to create a {test_type} Test with default summary".format(
                test_type=test_type
            )
        )

    test_ids = list(context.jaxa.tests.keys())

    TestSetActions.add_tests_to_testset(
        jaxa_client=context.jaxa.jaxa_client,
        testset_id=context.jaxa.active_testset_id,
        test_ids=test_ids,
    )


@then("the TestSet contains the tests")
def step_impl(context):
    response = TestSetActions.get_tests_in_testset(
        jaxa_client=context.jaxa.jaxa_client, testset_id=context.jaxa.active_testset_id
    )
    test_ids = [
        t.get("issueId") for t in response.get("getTestSet").get("tests").get("results")
    ]
    assert test_ids == list(context.jaxa.tests.keys())


@when("remove a Test from the TestSet")
def step_impl(context):
    response = TestSetActions.get_tests_in_testset(
        jaxa_client=context.jaxa.jaxa_client, testset_id=context.jaxa.active_testset_id
    )
    tests = {}
    for t in response.get("getTestSet").get("tests").get("results"):
        tests[t.get("issueId")] = {
            "summary": t.get("jira").get("summary"),
            "jira_key": t.get("jira").get("key"),
            "test_type": t.get("testType").get("name"),
        }

    removed_test_ids = []
    for row in context.table:
        test_type = row["test_type"]
        test_summary = row["test_summary"]
        for test_id, test_values in tests.items():
            if test_values.get("test_type") == test_type and test_values.get(
                "summary"
            ).startswith(test_summary):
                TestSetActions.remove_tests_from_testset(
                    jaxa_client=context.jaxa.jaxa_client,
                    testset_id=context.jaxa.active_testset_id,
                    test_ids=[test_id],
                )
                removed_test_ids.append(test_id)
                del context.jaxa.tests[test_id]

    assert removed_test_ids != []


@when("we search for TestSet using JQL {query}")
def step_impl(context, query):
    response = TestSetActions.get_testsets_by_jql(
        jaxa_client=context.jaxa.jaxa_client, jql=query
    )
    print(response)
    context.jaxa.record_query_results(results=response)


@then("TestSet search results are returned")
def step_impl(context):
    result_count = context.jaxa.query_results.get("getTestSets").get("total")
    print(result_count)
    assert result_count > 0


@then("TestSet query result contains expected TestSet")
def step_impl(context):
    testset_id = context.jaxa.active_testset_id
    for result in context.jaxa.query_results.get("getTestSets").get("results"):
        if testset_id == result.get("issueId"):
            # match
            break
    else:
        raise Exception(f"No match found in QueryResults for TestSet summary {summary}")
