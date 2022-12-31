class TestExecutionActions:
    @staticmethod
    def create_test_execution(
        *, jaxa_client, project_id: str, summary: str, test_ids: list
    ):
        response = jaxa_client.xray_gql.test_executions.create_test_execution(
            project_id=project_id, summary=summary, testenvs=[], test_ids=test_ids
        )
        print(response)
        return response

    @staticmethod
    def add_testexecution_to_testplan(
        *, jaxa_client, testplan_id: str, test_execution_ids: list
    ):
        response = jaxa_client.xray_gql.test_executions.add_testexecutions_to_testplan(
            testplan_id=testplan_id, testexecution_ids=test_execution_ids
        )
        print(response)
        return response
