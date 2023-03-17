import datetime
import os
import uuid

import pytest
from dotenv import load_dotenv

from jaxa import JAXAClient


@pytest.fixture()
def load_env():
    load_dotenv()


@pytest.fixture
def jaxa_client(load_env):
    return JAXAClient(
        rest_url=os.environ["JAXA_XRAY_BASEURL"],
        client_id=os.environ["JAXA_JIRA_CLIENT_ID"],
        client_secret=os.environ["JAXA_JIRA_CLIENT_SECRET"],
    )


@pytest.fixture()
def xray_seeders():
    yield XRaySeeders()


class XRaySeeders:
    @property
    def loaded_testplan(self):
        return self._loaded_testplan

    @property
    def new_tests(self):
        return self._new_tests

    def _loaded_testplan(self, jirasync_client, test_project_id, test_count: int = 4):
        uniq = str(uuid.uuid4())[:8]

        # create a test plan
        testplan_name = f"TestPlan {uniq} [{str(datetime.datetime.now())}]"
        testplan = jirasync_client.gql.test_plan.create_test_plan(
            project_id=test_project_id, summary=testplan_name
        )
        testplan_id = (
            jirasync_client.gql.test_plan.get_issueid_from_createtestplan_result(
                testplan
            )
        )

        # create some tests and assign them to test plan
        test_ids = self._new_tests(jirasync_client, test_project_id, test_count)

        # assign test to testplan
        jirasync_client.gql.test_plan.assign_tests_to_testplan(
            test_ids=test_ids, testplan_id=testplan_id
        )
        return testplan_id

    @staticmethod
    def _new_tests(jirasync_client, test_project_id, test_count: int = 4):
        uniq = str(uuid.uuid4())[:8]

        # create some tests and assign them to test plan
        test_ids = []
        for x in range(test_count):
            test = jirasync_client.gql.tests.create_generic_test(
                project_id=test_project_id,
                summary=f"[{x}] Test {uniq} [{str(datetime.datetime.now())}]",
                unstructured="",
            )
            test_ids.append(
                jirasync_client.gql.tests.get_issueid_from_createtest_result(test)
            )
        return test_ids
