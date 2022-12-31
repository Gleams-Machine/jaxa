from typing import List


class TestPlanActions:
    @staticmethod
    def create_test_plan(*, jaxa_client, project_id, sumamry):
        response = jaxa_client.xray_gql.test_plan.create_test_plan(
            project_id=project_id, summary=sumamry
        )
        return response

    @staticmethod
    def create_test_plan_with_tests(
        *, jaxa_client, project_id: str, summary: str, test_ids: List
    ):
        response = jaxa_client.xray_gql.test_plan.create_test_plan_with_tests(
            project_id=project_id, summary=summary, test_ids=test_ids
        )
        return response

    @staticmethod
    def get_testplan_from_id(*, jaxa_client, testplan_id: str):
        response = jaxa_client.xray_gql.test_plan.get_testplan_from_id(
            testplan_id=testplan_id
        )
        return response
