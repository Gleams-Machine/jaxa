import datetime
import uuid

from behave import *
from decouple import config

from features.steps.support import TestActions


@when("we opt to create a {test_type} Test with default summary")
def step_impl(context, test_type):
    uniq = str(uuid.uuid4())[:8]
    test_summary = f"Test: {uniq} [{str(datetime.datetime.now())}]"

    context.execute_steps(
        "when we opt to create a {test_type} Test with summary {test_summary}".format(
            test_type=test_type, test_summary=test_summary
        )
    )


@when("we opt to create a {test_type} Test with summary {test_summary}")
def step_impl(context, test_type, test_summary):
    test_project_id = config("JAXA_TEST_PROJECT_ID")

    if test_type.lower() == "cucumber":
        response = TestActions.create_cucumber_test(
            jaxa_client=context.jaxa.jaxa_client,
            project_id=test_project_id,
            summary=test_summary,
            gherkin="""
Given a test is described using the Gherkin language
When that test is read
Then it is supposed to be more readable!
""",
        )
    elif test_type.lower() == "manual":
        response = TestActions.create_manual_test(
            jaxa_client=context.jaxa.jaxa_client,
            project_id=test_project_id,
            summary=test_summary,
            steps=[
                {
                    "action": "Create first example step",
                    "result": "First step was created",
                },
                {
                    "action": "Create second example step with data",
                    "data": "Data for the step",
                    "result": "Second step was created with data",
                },
            ],
        )
    elif test_type.lower() == "generic":
        response = TestActions.create_generic_test(
            jaxa_client=context.jaxa.jaxa_client,
            project_id=test_project_id,
            summary=test_summary,
            unstructured="test steps",
        )
    else:
        raise Exception("Invalid value for test_type")

    test_id = response.get("createTest").get("test").get("issueId")
    test_key = response.get("createTest").get("test").get("jira").get("key")
    context.jaxa.record_test(test_id=test_id, test_key=test_key)


@then("a {test_type} Test is created")
def step_impl(context, test_type):
    current_test = context.jaxa.active_test_id
    print(f"Current Test: {current_test}")
    test_data = context.jaxa.tests[current_test]
    print(f"Test data: {test_data}")

    response = TestActions.get_test_from_jira_id(
        jaxa_client=context.jaxa.jaxa_client, jira_id=test_data.get("test_key")
    )
    test_types = [
        t.get("testType").get("name")
        for t in response.get("getTests", {}).get("results", [])
    ]
    assert test_types == [test_type]


@when("we search for Tests using JQL {query}")
def step_impl(context, query):
    response = TestActions.get_test_by_jql(
        jaxa_client=context.jaxa.jaxa_client, jql_query=query
    )
    print(response)
    context.jaxa.record_query_results(results=response)


@then("Test search results are returned")
def step_impl(context):
    result_count = context.jaxa.query_results.get("getTests").get("total")
    print(result_count)
    assert result_count > 0


@when("we add a Test to a TestPlan")
def step_impl(context):
    pass
