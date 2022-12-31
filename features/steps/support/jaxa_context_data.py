from dataclasses import dataclass, field
from typing import Dict, List

from decouple import config

from jaxa import JAXAClient


def get_jaxa_client():
    return JAXAClient(
        rest_url=config("JAXA_XRAY_CLOUD_REST_URL"),
        client_id=config("JAXA_JIRA_CLIENT_ID"),
        client_secret=config("JAXA_JIRA_CLIENT_SECRET"),
    )


@dataclass
class JAXAContextData:
    jaxa_client: JAXAClient = get_jaxa_client()
    tests: Dict = field(default_factory=lambda: {})
    testsets: Dict = field(default_factory=lambda: {})
    testplans: Dict = field(default_factory=lambda: {})
    testexecutions: Dict = field(default_factory=lambda: {})
    testruns: Dict = field(default_factory=lambda: {})
    query_results: Dict = field(default_factory=lambda: {})
    active_testplan_id: str = ""
    active_test_id: str = ""
    active_testset_id: str = ""
    active_testexecution_id: str = ""
    active_testruns_id: str = ""

    def record_testplan(self, *, testplan_id: str, testplan_key: str) -> None:
        self.testplans[testplan_id] = {
            "testplan_id": testplan_id,
            "testplan_key": testplan_key,
        }
        self.active_testplan_id = testplan_id

    def record_test(self, *, test_id: str, test_key: str) -> None:
        print(f"recording test info: {test_id}, {test_key}")
        self.tests[test_id] = {"test_id": test_id, "test_key": test_key}
        self.active_test_id = test_id

    def record_testset(
        self, *, testset_id: str, testset_key: str, summary: str = ""
    ) -> None:
        print(f"recording testset info: {testset_id}, {testset_key}")
        self.testsets[testset_id] = {
            "testset_id": testset_id,
            "testset_key": testset_key,
            "summary": summary,
        }
        self.active_testset_id = testset_id

    def record_testexecution(
        self, *, testexecution_id: str, testexecution_key: str, summary: str = ""
    ) -> None:
        print(f"recording testexecution info: {testexecution_id}, {testexecution_key}")
        self.testexecutions[testexecution_id] = {
            "testexecution_id": testexecution_id,
            "testexecution_key": testexecution_key,
            "summary": summary,
        }
        self.active_testexecution_id = testexecution_id

    def record_testrun(
        self, *, testrun_id: str, test_id: str, testexecution_id: str
    ) -> None:
        print(f"recording testrun info: {testrun_id}")
        self.testruns[testrun_id] = {
            "testrun_id": testrun_id,
            "test_id": test_id,
            "testexecution_id": testexecution_id,
        }
        self.active_testruns_id = testrun_id

    def record_test_ids(self, *, test_ids: List) -> None:
        for test_id in test_ids:
            self.tests[test_id] = {
                "test_id": test_id,
            }

    def record_query_results(self, *, results) -> None:
        self.query_results = results


class JaxaContextInitialiser:
    def __init__(self, *, context):
        context.jaxa = JAXAContextData()
