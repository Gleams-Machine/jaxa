import datetime
import uuid
from decouple import config
from behave import *
from features.steps.support import TestExecutionActions


@when(u'we opt to create a TestExecution')
def step_impl(context):
    project_id = config("JAXA_TEST_PROJECT_ID")
    uniq = str(uuid.uuid4())[:8]
    summary = f"TestExecution: {uniq} [{str(datetime.datetime.now())}]"
    test_id = context.jaxa.active_test_id
    response = TestExecutionActions.create_test_execution(
        jaxa_client=context.jaxa.jaxa_client,
        project_id=project_id,
        summary=summary,
        test_ids=[test_id]
    )
    testexecution_id = response.get("createTestExecution").get("testExecution").get("issueId")
    testexecution_key = response.get("createTestExecution").get("testExecution").get("jira").get("key")
    testexecution_summary = response.get("createTestExecution").get("testExecution").get("jira").get("summary")
    context.jaxa.record_testexecution(
        testexecution_id=testexecution_id,
        testexecution_key=testexecution_key,
        summary=testexecution_summary
    )
    print('debug')


@when(u'we add a TestExecution to a TestPlan')
def step_impl(context):
    testexecution_id = context.jaxa.active_testexecution_id
    testplan_id = context.jaxa.active_testplan_id
    response = TestExecutionActions.add_testexecution_to_testplan(
        jaxa_client=context.jaxa.jaxa_client,
        testplan_id=testplan_id,
        test_execution_ids=[testexecution_id],
    )
    print('debug')

