class TestRunActions:
    @staticmethod
    def get_test_runs(*, jaxa_client, test_ids: list, testexecution_ids: list):
        response = jaxa_client.xray_gql.test_runs.get_test_runs(
            testissue_ids=test_ids, testExecIssueIds=testexecution_ids
        )
        print(response)
        return response

    @staticmethod
    def set_testrun_status(*, jaxa_client, testrun_id: str, status: str):
        response = jaxa_client.xray_gql.test_runs.update_testrun_status(
            testrun_id=testrun_id, status=status
        )
        print(response)
        return response
