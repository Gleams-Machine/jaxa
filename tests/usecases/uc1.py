"""
UC1:
Context:
- Tests executed in CI.
- We do not have an existing TestPlan
- We know what tests we have executed and their corresponding execution results
Steps needed:
- For each test
    -- check if test exists or not based on content
        (but how do we get content from pytest json?)
    -- stick with name for now. limit of 255

     name = nodeid
     status = outcome if != 'skipped'

https://xray.cloud.getxray.app/doc/graphql/updatetestrun.doc.html

https://docs.getxray.app/display/XRAYCLOUD/GraphQL+API

"""
import datetime
import json
import logging
import uuid
from pathlib import Path
from typing import Dict, List

from decouple import config

from jaxa import JAXAClient

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("gql.transport.requests").setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
log = logging.getLogger()

LINE_LENGTH = 40


class OperationalWarnings(Exception):
    pass


class OperationalFailure(Exception):
    pass


class ProcessTestExecutionData:
    def __init__(self, *, filename: str, project_id: str):
        self._filename = filename
        self._project_id = project_id
        self._uniqueness = f"{str(uuid.uuid4())[:8]} [{str(datetime.datetime.now())}]"
        self._execution_data = self._load_execution_data()
        self._suite_data = self._build_test_suite_data()
        self._jaxa_client = JAXAClient(
            rest_url=config("JAXA_XRAY_BASEURL"),
            client_id=config("JAXA_JIRA_CLIENT_ID"),
            client_secret=config("JAXA_JIRA_CLIENT_SECRET"),
        )

    def process(self):
        log.info("=" * LINE_LENGTH)
        start = datetime.datetime.now()
        results = [
            self._process_single_test(test_data=t_data)
            for t_data in self._execution_data.get("tests")
        ]

        log.info("-" * LINE_LENGTH)
        test_ids = [r.get("test_id") for r in results]
        testexecution_ids = [r.get("testexecution_id") for r in results]

        testplan_id, _ = self._create_testplan_with_tests(test_ids=test_ids)
        self._add_testexecutions_to_testplan(
            testplan_id=testplan_id, testexecution_ids=testexecution_ids
        )

        end = datetime.datetime.now()
        log.info(f"Processing duration: {end - start}")
        log.info("=" * LINE_LENGTH)

    def _process_single_test(self, *, test_data: Dict):
        test_summary = test_data.get("nodeid")
        log.info("-" * LINE_LENGTH)

        test_id, test_key = self._get_or_create_test(testname=test_summary)

        testexecution_id, testexecution_key = self._create_testexecution(
            test_id=test_id
        )

        testrun_id = self._create_testrun_with_status(
            test_id=test_id,
            testexecution_id=testexecution_id,
            status=test_data.get("outcome"),
        )

        self._update_testrun_comment(testrun_id=testrun_id)

        return {
            "test_id": test_id,
            "test_key": test_key,
            "testexecution_id": testexecution_id,
            "testexecution_key": testexecution_key,
            "testrun_id": testrun_id,
        }

    def _load_execution_data(self):
        log.info(f"Loading Test Execution data from: {self._filename}")
        with open(self._filename) as f:
            return json.load(f)

    def _build_test_suite_data(self):
        environment_data = self._execution_data.get("environment")
        suite_data = {
            "created": self._execution_data.get("created"),
            "duration": self._execution_data.get("duration"),
            "root": self._execution_data.get("root"),
            "summary": self._execution_data.get("summary"),
            "uuid": "",
        }
        return {"environment": environment_data, "suite": suite_data}

    def _get_or_create_test(self, *, testname: str, testtype: str = "pyAutomated"):
        # See: https://jira.atlassian.com/browse/JRASERVER-25092
        log.info(f"[TEST] Processing test ({testname})")
        test_id = None
        test_key = None
        try:
            log.debug("Determining if Test with summary ({testname}) exists")
            jql_testname = testname.replace("[", "\\\\[").replace("]", "\\\\]")
            query = (
                f'project = "{self._project_id}" AND testType = {testtype} '
                f'AND summary ~ "{jql_testname}" ORDER BY created DESC'
            )
            results = self._jaxa_client.xray_gql.tests.get_tests_by_jql(jql_query=query)
            log.debug(results)
            tests = results.get("getTests").get("results")
            # Double check all results are for supplied testname.
            # There have been some cases where the results do not match if char >
            # or < is the only difference.
            tests = [t for t in tests if t.get("jira").get("summary") == testname]
            if tests:
                test_id = tests[0].get("issueId")
                test_key = tests[0].get("jira").get("key")
            else:
                # create a test
                test = self._jaxa_client.xray_gql.tests.create_pyautomated_test(
                    project_id=project_id, summary=testname, unstructured=""
                )
                warnings = test.get("createTest").get("warnings")
                if warnings:
                    raise OperationalWarnings(
                        f"createTest generated following warnings: {warnings}"
                    )
                test_id = test.get("createTest").get("test").get("issueId")
                test_key = test.get("createTest").get("test").get("jira").get("key")
                log.debug(f"Created new Test with ID: {test_id}")
        except Exception as exc:
            log.exception(exc)
        finally:
            log.info(f"[TEST] id={test_id} ; key={test_key}")
            return test_id, test_key

    def _create_testexecution(self, *, test_id: str):
        # create a test execution
        test_execution = (
            self._jaxa_client.xray_gql.test_executions.create_test_execution(
                project_id=self._project_id,
                summary=f"TestExecution: {self._uniqueness}",
                testenvs=[],
                test_ids=[test_id],
            )
        )
        warnings = test_execution.get("createTestExecution").get("warnings")
        if warnings:
            raise OperationalWarnings(
                f"createTestExecution generated following warnings: {warnings}"
            )

        testexecution_id = (
            test_execution.get("createTestExecution")
            .get("testExecution")
            .get("issueId")
        )
        testexecution_key = (
            test_execution.get("createTestExecution")
            .get("testExecution")
            .get("jira")
            .get("key")
        )
        log.info(f"[TEST EXECUTION] id={testexecution_id} ; key={testexecution_key}")
        return testexecution_id, testexecution_key

    def _create_testrun_with_status(
        self, *, test_id: str, testexecution_id: str, status: str
    ):
        # create a test run
        testrun = self._jaxa_client.xray_gql.test_runs.get_test_runs(
            testissue_ids=[test_id], testExecIssueIds=[testexecution_id]
        )
        testrun_id = testrun.get("getTestRuns").get("results")[0].get("id")
        log.info(f"[TEST RUN] id={testrun_id}")

        # set status
        testrun_status = self._jaxa_client.xray_gql.test_runs.update_testrun_status(
            testrun_id=testrun_id, status=status
        )
        op_status = testrun_status.get("updateTestRunStatus")
        if op_status != "Success":
            raise OperationalFailure(
                f"updateTestRunStatus generated following status: {op_status}"
            )
        log.info(f"[TEST RUN] status={op_status}")
        return testrun_id

    def _update_testrun_comment(self, *, testrun_id: str):
        # see: https://jira.atlassian.com/secure/WikiRendererHelpAction.jspa?section=all
        comment = (
            "h3. Suite Data\n\n{code:json}"
            + json.dumps(self._suite_data, indent=4)
            + "{code}\n\n"
        )
        testrun_comment = self._jaxa_client.xray_gql.test_runs.add_testrun_comment(
            testrun_id=testrun_id, comment=comment
        )
        op_status = testrun_comment.get("updateTestRunComment")
        if op_status != "Success":
            raise OperationalFailure(
                f"updateTestRunComment generated following status: {op_status}"
            )

    def _create_testplan_with_tests(self, *, test_ids):
        response = self._jaxa_client.xray_gql.test_plan.create_test_plan_with_tests(
            project_id=self._project_id,
            summary=f"TestPlan: {self._uniqueness}",
            test_ids=test_ids,
        )
        testplan_id = response.get("createTestPlan").get("testPlan").get("issueId")
        testplan_key = (
            response.get("createTestPlan").get("testPlan").get("jira").get("key")
        )
        log.info(f"[TEST PLAN] id={testplan_id} ; key={testplan_key}")
        log.info(f"[TEST PLAN] test-ids={test_ids}")
        return testplan_id, testplan_key

    def _add_testexecutions_to_testplan(
        self, *, testplan_id: str, testexecution_ids: List
    ):
        response = (
            self._jaxa_client.xray_gql.test_executions.add_testexecutions_to_testplan(
                testplan_id=testplan_id, testexecution_ids=testexecution_ids
            )
        )
        log.info(f"[TEST PLAN] testexecution-ids={testexecution_ids}")
        warnings = response.get("addTestExecutionsToTestPlan").get("warnings")
        if warnings:
            raise OperationalWarnings(
                f"addTestExecutionsToTestPlan generated following warnings: {warnings}"
            )

    def _prepare_testrun_timing_data(*, created: float, duration: float):
        ts_format = "%Y-%m-%dT%H:%M:%SZ"
        started = datetime.datetime.fromtimestamp(created)
        finished = started + datetime.timedelta(seconds=duration)
        return started.strftime(ts_format), finished.strftime(ts_format)

    def _set_testrun_timing(self, *, testrun_id: str, started_on: str, finished_on):
        testrun_comment = self._jaxa_client.xray_gql.test_runs.update_testrun_timing(
            testrun_id=testrun_id, started_on=started_on, finished_on=finished_on
        )
        warnings = testrun_comment.get("updateTestRun").get("warnings")
        if warnings:
            raise OperationalWarnings(
                f"updateTestRun generated following warnings: {warnings}"
            )


if __name__ == "__main__":
    filename = Path(__file__).parent / "json_data" / "uc1_report_1.json"
    project_id = "QD"
    ProcessTestExecutionData(project_id=project_id, filename=filename).process()
