"""
Jira Xray API categories
"""
import os

from rich.console import Console
from rich.table import Table

from ...api.graphql import load_query_from_file
from ...api.rest import HTTPMethods, MetaCategory
from ...utils import log

THIS_DIR = os.path.dirname(__file__)
GQL_QUERY_DIR = "../xray/gql_templates"


class Authenticate(MetaCategory):
    """https://docs.getxray.app/display/XRAYCLOUD/Authentication+-+REST"""

    def get_auth_token(self, client_id: str, client_secret: str) -> str:
        """
        Requests the Auth Token required for subsequent API calls
        :param client_id:
            The client id configured in Jira XRay Global settings
        :param client_secret:
            The client secret configured in Jira XRay Global settings
        :return: str
            ex: "eykdbvdshjfgsdkjfsdlkf.eyjgdskjfbdsjfgdhgdlhfdsbfbdfvdksbvdksbjv"
        """
        log.debug("Getting auth token")
        data = dict(client_id=client_id, client_secret=client_secret)
        return self._session.request(HTTPMethods.POST, "api/v1/authenticate", json=data)


class GQLTests(MetaCategory):
    """https://docs.getxray.app/display/XRAYCLOUD/Authentication+-+REST"""

    template_dir = "tests"

    @staticmethod
    def get_issueid_from_createtest_result(result):
        return result.get("createTest", {}).get("test", {}).get("issueId", "")

    @staticmethod
    def get_jirakeyid_from_createtest_result(result):
        return (
            result.get("createTest", {}).get("test", {}).get("jira", {}).get("key", "")
        )

    def get_test_from_jira_id(self, jira_id: str) -> dict:
        """
        Perform graphQL call to get tests using a JQL query
        :param jira_id:
            The JQL query used to find tests. E.g. project=QADemo
        :return: dict
            ex: {"getTests": {"results": []}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "get_test_by_jira_id.graphql",
            )
        )
        variables = dict(jira_id=f"key={jira_id}")
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        return response

    def get_tests_by_jql(self, jql_query: str) -> dict:
        """
        Perform graphQL call to get tests using a JQL query
        :param jql_query:
            The JQL query used to find tests. E.g. project=QADemo
        :return: dict
            ex: {"getTests": {"results": []}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR, GQL_QUERY_DIR, self.template_dir, "get_tests_by_jql.graphql"
            )
        )
        variables = dict(jql_query=jql_query)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        return response

    def create_cucumber_test(self, project_id: str, summary: str, gherkin: str) -> dict:
        """
        Perform graphQL mutation to create a Cucumber test
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        :param gherkin:
            The gherkin syntax of the test
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "create_cucumber_test.graphql",
            )
        )
        variables = dict(project_id=project_id, summary=summary, gherkin=gherkin)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")

        test_issue_id = self.get_issueid_from_createtest_result(response)
        test_jira_id = self.get_jirakeyid_from_createtest_result(response)
        log.debug(
            f"Created Cucumber Test with XRay ID [{test_issue_id}] and Jira ID [{test_jira_id}]"
        )
        return response

    def create_generic_test(
        self, project_id: str, summary: str, unstructured: str
    ) -> dict:
        """
        Perform graphQL mutation to create a Cucumber test
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        :param unstructured:
            The unstructured syntax of the test
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "create_generic_test.graphql",
            )
        )
        variables = dict(
            project_id=project_id, summary=summary, unstructured=unstructured
        )
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        test_issue_id = self.get_issueid_from_createtest_result(response)
        test_jira_id = self.get_jirakeyid_from_createtest_result(response)
        log.debug(
            f"Created Generic Test with XRay ID [{test_issue_id}] and Jira ID [{test_jira_id}]"
        )
        return response

    def create_pyautomated_test(
        self, project_id: str, summary: str, unstructured: str
    ) -> dict:
        """
        Perform graphQL mutation to create a pyAutomated type test
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        :param unstructured:
            The unstructured syntax of the test
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "create_pyautomated_test.graphql",
            )
        )
        variables = dict(
            project_id=project_id, summary=summary, unstructured=unstructured
        )
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        test_issue_id = self.get_issueid_from_createtest_result(response)
        test_jira_id = self.get_jirakeyid_from_createtest_result(response)
        log.debug(
            f"Created pyAutomated Test with XRay ID [{test_issue_id}] and Jira ID [{test_jira_id}]"
        )
        return response

    def create_manual_test(self, project_id: str, summary: str, steps: list) -> dict:
        """
        Perform graphQL mutation to create a Cucumber test
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        :param seps:
            The steps of the test
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR, GQL_QUERY_DIR, self.template_dir, "create_manual_test.graphql"
            )
        )
        variables = dict(project_id=project_id, summary=summary, steps=steps)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        test_issue_id = self.get_issueid_from_createtest_result(response)
        test_jira_id = self.get_jirakeyid_from_createtest_result(response)
        log.debug(
            f"Created Manual Test with XRay ID [{test_issue_id}] and Jira ID [{test_jira_id}]"
        )
        return response


class GQLTestPlan(MetaCategory):
    """https://docs.getxray.app/display/XRAYCLOUD/Authentication+-+REST"""

    template_dir = "testplans"

    @staticmethod
    def get_issueid_from_createtestplan_result(result):
        return result.get("createTestPlan", {}).get("testPlan", {}).get("issueId", "")

    @staticmethod
    def get_jirakeyid_from_createtestplan_result(result):
        return (
            result.get("createTestPlan", {})
            .get("testPlan", {})
            .get("jira", {})
            .get("key", "")
        )

    @staticmethod
    def get_test_issueids_from_gettestplan_result(response):
        return [
            test_result.get("issueId", "")
            for test_result in response.get("getTestPlan", {})
            .get("tests", {})
            .get("results", [])
        ]

    @staticmethod
    def get_test_jiraids_from_gettestplan_result(response):
        return [
            test_result.get("jira", {}).get("key", "")
            for test_result in response.get("getTestPlan", {})
            .get("tests", {})
            .get("results", [])
        ]

    @staticmethod
    def summarise_testplan_tests(response):
        testplan_id = response.get("getTestPlan", {}).get("issueId", "")
        testplan_jira_id = (
            response.get("getTestPlan", {}).get("jira", {}).get("key", "")
        )
        table = Table(title=f"Test Plan : {testplan_jira_id} [{testplan_id}]")
        table.add_column("Test Jira ID", style="cyan", justify="left")
        table.add_column("Test Summary", style="cyan", justify="left")
        table.add_column("XRay ID", style="cyan", justify="right")
        for test_result in (
            response.get("getTestPlan", {}).get("tests", {}).get("results", [])
        ):
            jira_key = test_result.get("jira", {}).get("key", "")
            jira_summary = test_result.get("jira", {}).get("summary", "")
            xray_id = test_result.get("issueId", {})
            table.add_row(jira_key, jira_summary, xray_id)
        console = Console()
        console.print(table)

    @staticmethod
    def summarise_testplan_execution_runs(response):
        testplan_id = response.get("getTestPlan", {}).get("issueId", "")
        table = Table(title=f"Test Plan : {testplan_id}")
        table.add_column("Test Jira ID", style="cyan", justify="left")
        table.add_column("Test Summary", style="cyan", justify="left")
        table.add_column("Execution Status", style="cyan", justify="right")
        for testexec_result in (
            response.get("getTestPlan", {}).get("testExecutions", {}).get("results", [])
        ):
            for testrun_result in testexec_result.get("testRuns", {}).get(
                "results", []
            ):
                jira_key = testrun_result.get("test", {}).get("jira", {}).get("key", "")
                jira_summary = (
                    testrun_result.get("test", {}).get("jira", {}).get("summary", "")
                )
                test_status = testrun_result.get("status", {}).get("name", "")
                table.add_row(jira_key, jira_summary, test_status)
        console = Console()
        console.print(table)

    def get_testplan_from_id(self, *, testplan_id: str) -> dict:
        """
        Perform graphQL call to get tests using a JQL query
        :param jql_query:
            The JQL query used to find tests. E.g. project=QADemo
        :return: dict
            ex: {"getTests": {"results": []}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "get_testplan_from_id.graphql",
            )
        )
        variables = dict(testplan_id=testplan_id)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        return response

    def get_testplan_by_jql(self, *, jql_query: str) -> dict:
        """ """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "get_testplan_by_jql.graphql",
            )
        )
        variables = dict(jql_query=jql_query)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        return response

    def create_test_plan(self, *, project_id: str, summary: str) -> dict:
        """
        Perform graphQL mutation to create a Test Plan
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "create_empty_testplan.graphql",
            )
        )
        variables = dict(project_key=project_id, summary=summary)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        issue_id = self.get_issueid_from_createtestplan_result(result=response)
        jira_id = self.get_jirakeyid_from_createtestplan_result(result=response)
        log.debug(f"Created TestPlan {jira_id} [{issue_id}]")
        return response

    def create_test_plan_with_tests(
        self, *, project_id: str, summary: str, test_ids: str
    ) -> dict:
        """
        Perform graphQL mutation to create a Test Plan
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "create_testplan_with_tests.graphql",
            )
        )
        variables = dict(project_key=project_id, summary=summary, test_ids=test_ids)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        issue_id = self.get_issueid_from_createtestplan_result(result=response)
        jira_id = self.get_jirakeyid_from_createtestplan_result(result=response)
        log.debug(f"Created TestPlan {jira_id} [{issue_id}]")
        log.debug(f"Assigned Tests {test_ids} to TestPlan {issue_id}")
        return response

    def assign_tests_to_testplan(self, *, testplan_id: str, test_ids: list) -> dict:
        """
        Perform graphQL mutation to create a Test Plan
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "assign_tests_to_existing_testplan.graphql",
            )
        )
        variables = dict(testplan_id=testplan_id, test_ids=test_ids)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        log.debug(f"Assigned Tests {test_ids} to TestPlan {testplan_id}")
        return response


class GQLTestExecution(MetaCategory):
    """https://xray.cloud.getxray.app/doc/graphql/createtestexecution.doc.html"""

    template_dir = "testexecutions"

    def get_issueid_from_createtestexecution_result(self, *, result):
        return (
            result.get("createTestExecution", {})
            .get("testExecution", {})
            .get("issueId", "")
        )

    def get_jirakeyid_from_createtestexecution_result(self, *, result):
        return (
            result.get("createTestExecution", {})
            .get("testExecution", {})
            .get("jira", {})
            .get("key", "")
        )

    def get_testexecutions_by_jql(self, *, jql: str) -> dict:
        """
        Perform graphQL mutation to create a Test Plan
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "get_testexecutions_by_jql.graphql",
            )
        )
        variables = dict(jql=jql)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        return response

    def create_test_execution(
        self, *, project_id: str, summary: str, testenvs: list, test_ids: list
    ) -> dict:
        """
        Perform graphQL mutation to create a Test Plan
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        more args here
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "create_testexecution.graphql",
            )
        )
        variables = dict(
            project_id=project_id, summary=summary, testenvs=testenvs, test_ids=test_ids
        )
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        log.debug(f"Created TestExecution for Tests {test_ids}")
        return response

    def add_testexecutions_to_testplan(
        self, *, testplan_id: str, testexecution_ids: list
    ) -> dict:
        """
        Perform graphQL mutation to create a Test Plan
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "add_testexecutions_to_testplan.graphql",
            )
        )
        variables = dict(testplan_id=testplan_id, testexecution_ids=testexecution_ids)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        log.debug(f"Added TestExecution {testexecution_ids} to TestPlan {testplan_id}")
        return response


class GQLTestRun(MetaCategory):
    """https://xray.cloud.getxray.app/doc/graphql/updatetestrunstatus.doc.html"""

    template_dir = "testruns"

    @staticmethod
    def get_testrunid_from_gettestruns_result(*, result):
        return result.get("getTestRuns", {}).get("results", [])[0].get("id")

    @staticmethod
    def get_status_from_gettestrunsbyid_result(*, result):
        return [
            res.get("status", {}).get("name", "")
            for res in result.get("getTestRunsById", {}).get("results", [])
        ]

    def get_test_runs(self, *, testissue_ids, testExecIssueIds):
        query = load_query_from_file(
            os.path.join(
                THIS_DIR, GQL_QUERY_DIR, self.template_dir, "get_testruns.graphql"
            )
        )
        variables = dict(testIssueIds=testissue_ids, testExecIssueIds=testExecIssueIds)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        return response

    def get_testruns_by_id(self, *, testrun_ids: list):
        query = load_query_from_file(
            os.path.join(
                THIS_DIR, GQL_QUERY_DIR, self.template_dir, "get_testruns_by_id.graphql"
            )
        )
        variables = dict(testrun_ids=testrun_ids)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        return response

    def update_testrun_status(self, *, testrun_id: str, status: str) -> dict:
        """
        Perform graphQL mutation to create a Test Plan
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}
        """
        status = status.upper()
        valid_statuses = [
            status.get("name")
            for status in GQLTestStatus(self._session)
            .get_teststatuses()
            .get("getStatuses")
        ]
        if status not in valid_statuses:
            # TODO: Custom exception please
            raise Exception(
                f"Invalid value for TestRun status [{status}]. Valid values {valid_statuses}"
            )
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "update_testrun_status.graphql",
            )
        )
        variables = dict(testrun_id=testrun_id, status=status)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        log.debug(f"Updated Test Run status {testrun_id} to: {status}")
        return response

    def update_testrun_timing(
        self, *, testrun_id: str, started_on: str, finished_on
    ) -> dict:
        """
        Perform graphQL mutation to create a Test Plan
        :param project_id:
            The Jira project to create the test in
        :param summary:
            The Test ticket summary field
        :return: dict
            ex: {"createTest": {"test": {"jira": {"key": ...}}}}

        startedOn: "2020-03-09T10:35:09Z",
        finishedOn: "2020-04-09T10:35:09Z"
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "update_testrun_timing.graphql",
            )
        )
        variables = dict(
            testrun_id=testrun_id, startedon=started_on, finishedon=finished_on
        )
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        log.debug(f"Updated Test Run Timing {testrun_id}")
        return response

    def add_testrun_comment(self, *, testrun_id: str, comment: str) -> dict:
        """
        Perform graphQL mutation to add a comment to a Test Run

        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "add_testrun_comment.graphql",
            )
        )
        variables = dict(testrun_id=testrun_id, comment=comment)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        log.debug(f"Updated Test Run comment {testrun_id}")
        return response


class GQLTestSets(MetaCategory):
    """https://xray.cloud.getxray.app/doc/graphql/updatetestrunstatus.doc.html"""

    template_dir = "testsets"

    @staticmethod
    def get_testsetid_from_createtestset_result(*, result):
        return result.get("createTestSet", {}).get("testSet", {}).get("issueId")

    @staticmethod
    def get_jiraid_from_createtestset_result(*, result):
        return (
            result.get("createTestSet", {})
            .get("testSet", {})
            .get("jira", {})
            .get("key", "")
        )

    @staticmethod
    def get_test_issue_ids_from_gettestset_result(*, result):
        return [
            test.get("issueId", "")
            for test in result.get("getTestSet", {}).get("tests", {}).get("results", [])
        ]

    @staticmethod
    def display_testset_tests(*, response):
        testset_id = response.get("getTestSet", {}).get("jira", {}).get("key")
        testset_summary = response.get("getTestSet", {}).get("jira", {}).get("summary")
        table = Table(
            title=f"Test Set : {testset_id}",
            caption=testset_summary,
            style="on blue",
            row_styles=["dim", ""],
        )
        table.add_column("Test Jira ID", justify="left")
        table.add_column("Test Summary", justify="left")
        table.add_column("Test Type", justify="right")
        for test_result in (
            response.get("getTestSet", {}).get("tests", {}).get("results", [])
        ):
            jira_key = test_result.get("jira", {}).get("key", "")
            jira_summary = test_result.get("jira", {}).get("summary", "")
            test_type = test_result.get("testType", {}).get("name", "")
            table.add_row(jira_key, jira_summary, test_type)
        console = Console()
        console.print(table)

    def get_tests_in_testset(self, *, testset_id: str):
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "get_tests_in_testset.graphql",
            )
        )
        variables = dict(testset_id=testset_id)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        # TODO: Deal with tests returned from query and format nicely
        log.debug(f"For TestSet {testset_id} the following tests are assigned: ")
        return response

    def add_tests_to_testset(self, *, testset_id: str, test_ids: list):
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "add_tests_to_testset.graphql",
            )
        )
        variables = dict(testset_id=testset_id, test_ids=test_ids)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        log.debug(f"Added Tests {test_ids} to TestSet {testset_id}")
        return response

    def remove_tests_from_testset(self, *, testset_id: str, test_ids: list):
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "remove_tests_from_testset.graphql",
            )
        )
        variables = dict(testset_id=testset_id, test_ids=test_ids)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        log.debug(f"Removed Tests {test_ids} from TestSet {testset_id}")
        return response

    def create_testset_with_tests(
        self, *, summary: str, project_key: str, test_ids: list
    ):
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "create_testset_with_tests.graphql",
            )
        )
        variables = dict(summary=summary, project_key=project_key, test_ids=test_ids)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        testset_id = self.get_testsetid_from_createtestset_result(result=response)
        testset_jira_id = self.get_jiraid_from_createtestset_result(result=response)
        log.debug(
            f"Created TestSet {testset_jira_id} [{testset_id}] with Tests {test_ids}"
        )
        return response

    def create_empty_testset(self, *, summary: str, project_key: str):
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "create_empty_testset.graphql",
            )
        )
        variables = dict(summary=summary, project_key=project_key)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        testset_id = self.get_testsetid_from_createtestset_result(result=response)
        testset_jira_id = self.get_jiraid_from_createtestset_result(result=response)
        log.debug(f"Created TestSet {testset_jira_id} [{testset_id}]")
        return response

    def get_testsets_by_jql(self, jql: str) -> dict:
        """
        Perform graphQL call to get tests using a JQL query
        :param jql:
            The JQL query used to find tests. E.g. project=QADemo
        :return: dict
            ex: {"getTests": {"results": []}}
        """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR,
                GQL_QUERY_DIR,
                self.template_dir,
                "get_testsets_by_jql.graphql",
            )
        )
        variables = dict(jql_query=jql)
        log.debug(f"Executing gql {query=} with {variables=}")
        response = self._session.execute_query(query, variables=variables)
        log.debug(f"GQL {response=}")
        return response


class GQLTestStatus(MetaCategory):
    template_dir = "teststatuses"

    def get_teststatuses(self) -> dict:
        """ """
        query = load_query_from_file(
            os.path.join(
                THIS_DIR, GQL_QUERY_DIR, self.template_dir, "get_test_statuses.graphql"
            )
        )
        log.debug(f"Executing gql {query=}")
        response = self._session.execute_query(query)
        log.debug(f"GQL {response=}")
        return response