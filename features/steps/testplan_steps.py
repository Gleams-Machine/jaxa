import datetime
import uuid
from decouple import config
from behave import *
from features.steps.support import TestPlanActions, TestActions


@when('we opt to create an empty TestPlan')
def step_impl(context):
    uniq = str(uuid.uuid4())[:8]
    test_project_id = config("JAXA_TEST_PROJECT_ID")
    summary = f"TestPlan: {uniq} [{str(datetime.datetime.now())}]"

    response = TestPlanActions.create_test_plan(
        jaxa_client=context.jaxa.jaxa_client,
        project_id=test_project_id,
        sumamry=summary
    )
    testplan_id = response.get("createTestPlan").get("testPlan").get("issueId")
    testplan_key = response.get("createTestPlan").get("testPlan").get("jira").get("key")
    context.jaxa.record_testplan(testplan_id=testplan_id, testplan_key=testplan_key)


@then('a TestPlan is created with no tests')
def step_impl(context):
    response = TestPlanActions.get_testplan_from_id(
        jaxa_client=context.jaxa.jaxa_client,
        testplan_id=context.jaxa.active_testplan_id
    )
    test_ids = response.get("getTestPlan", {}).get("tests", {}).get("results")
    assert test_ids == []


@when(u'we opt to create a TestPlan with tests')
def step_impl(context):
    uniq = str(uuid.uuid4())[:8]
    test_project_id = config("JAXA_TEST_PROJECT_ID")
    test_ids = []
    for row in context.table:
        test_type = row["test_type"]
        test_summary = f"{row['test_summary']} {uniq} [{str(datetime.datetime.now())}]"
        if test_type.lower() == "cucumber":
            response = TestActions.create_cucumber_test(
                jaxa_client=context.jaxa.jaxa_client,
                project_id=test_project_id,
                summary=test_summary,
                gherkin="""
            Given a test iis described using the Gherkin language
            When that test is read
            Then it is supposed to be more readable!
                    """
            )
        elif test_type.lower() == "manual":
            response = TestActions.create_manual_test(
                jaxa_client=context.jaxa.jaxa_client,
                project_id=test_project_id,
                summary=test_summary,
                steps=[
                    {
                        "action": "Create first example step",
                        "result": "First step was created"
                    },
                    {
                        "action": "Create second example step with data",
                        "data": "Data for the step",
                        "result": "Second step was created with data"
                    }
                ]
            )
        elif test_type.lower() == "generic":
            response = TestActions.create_generic_test(
                jaxa_client=context.jaxa.jaxa_client,
                project_id=test_project_id,
                summary=test_summary,
                unstructured="test steps"
            )
        else:
            raise Exception("Invalid value for test_type")

        test_ids.append(response.get("createTest").get("test").get("issueId"))

        response = TestPlanActions.create_test_plan_with_tests(
            jaxa_client=context.jaxa.jaxa_client,
            project_id=test_project_id,
            summary=f"TestPlan: {uniq} [{str(datetime.datetime.now())}]",
            test_ids=test_ids
        )
        testplan_id = response.get("createTestPlan").get("testPlan").get("issueId")
        testplan_key = response.get("createTestPlan").get("testPlan").get("jira").get("key")
        context.jaxa.record_testplan(testplan_id=testplan_id, testplan_key=testplan_key)
        context.jaxa.record_test_ids(test_ids=test_ids)


@then(u'a TestPlan is created with the tests')
def step_impl(context):
    response = TestPlanActions.get_testplan_from_id(
        jaxa_client=context.jaxa.jaxa_client,
        testplan_id=context.jaxa.active_testplan_id
    )
    test_ids = [t.get("issueId") for t in response.get("getTestPlan", {}).get("tests", {}).get("results")]
    assert test_ids == list(context.jaxa.tests.keys())
