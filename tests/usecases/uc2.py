"""
Given a Test Plan ID, get pyautomated tests list for sending to pytest

Should this be a plugin?

in framework we need to get tests (via an api - future?) in order to know what to execute
instead of passing in a big list of tests.

So an API like

GET /testplan/TP-1234/tests?testType=pyAutomated

Need to look into a fastapi svc for this.
caching?
auth?
ddb as backup?

"""

import logging
from pathlib import Path

from decouple import config

from jaxa import JAXAClient

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("gql.transport.requests").setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
log = logging.getLogger()


class TriggerTestExecution:
    def __init__(self, *, testplan_id: str):
        self._testplan_id = testplan_id
        self._jaxa_client = JAXAClient(
            rest_url=config("JAXA_XRAY_BASEURL"),
            client_id=config("JAXA_JIRA_CLIENT_ID"),
            client_secret=config("JAXA_JIRA_CLIENT_SECRET"),
        )

    def process(self):
        query = f"type = 'Test Plan' AND key = '{self._testplan_id}'"
        results = self._jaxa_client.xray_gql.test_plan.get_testplan_by_jql(
            jql_query=query
        )
        log.debug(results)
        tests = (
            results.get("getTestPlans").get("results")[0].get("tests").get("results")
        )
        # TODO: maybe use filter and map instead
        auto_tests = [
            t for t in tests if t.get("testType").get("name") == "pyAutomated"
        ]
        tests_to_execute = [t.get("jira").get("summary") for t in auto_tests]
        print(tests_to_execute)
        # get_testplan_by_jql
        # get_test_issueids_from_gettestplan_result


if __name__ == "__main__":
    filename = Path(__file__).parent / "json_data" / "uc1_report_1.json"
    testplan_id = "QD-2082"
    TriggerTestExecution(testplan_id=testplan_id).process()
