import datetime
import uuid
from decouple import config
from behave import *
from features.steps.support import TestRunActions


@when(u'we get TestRuns')
def step_impl(context):
    test_id = context.jaxa.active_test_id
    testexecution_id = context.jaxa.active_testexecution_id
    response = TestRunActions.get_test_runs(
        jaxa_client=context.jaxa.jaxa_client,
        test_ids=[test_id],
        testexecution_ids=[testexecution_id],
    )
    for testrun in response.get("getTestRuns").get("results"):
        testrun_id = testrun.get("id")
        context.jaxa.record_testrun(
            testrun_id=testrun_id,
            test_id=test_id,
            testexecution_id=testexecution_id
        )
        context.jaxa.active_testrun_id = testrun_id

    print('debug')


@when(u'we set the TestRun status to {status}')
def step_impl(context, status):
    testrun_id = context.jaxa.active_testrun_id
    response = TestRunActions.set_testrun_status(
        jaxa_client=context.jaxa.jaxa_client,
        testrun_id=testrun_id,
        status=status,
    )
    print('debug')

