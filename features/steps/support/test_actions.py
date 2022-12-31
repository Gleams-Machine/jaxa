class TestActions:
    @staticmethod
    def create_cucumber_test(
        *,
        jaxa_client,
        project_id,
        summary,
        gherkin,
    ):
        response = jaxa_client.xray_gql.tests.create_cucumber_test(
            project_id=project_id, summary=summary, gherkin=gherkin
        )
        return response

    @staticmethod
    def create_manual_test(
        *,
        jaxa_client,
        project_id,
        summary,
        steps,
    ):
        response = jaxa_client.xray_gql.tests.create_manual_test(
            project_id=project_id, summary=summary, steps=steps
        )
        return response

    @staticmethod
    def create_generic_test(
        *,
        jaxa_client,
        project_id,
        summary,
        unstructured,
    ):
        response = jaxa_client.xray_gql.tests.create_generic_test(
            project_id=project_id, summary=summary, unstructured=unstructured
        )
        return response

    @staticmethod
    def get_test_from_jira_id(*, jaxa_client, jira_id: str) -> dict:
        response = jaxa_client.xray_gql.tests.get_test_from_jira_id(jira_id=jira_id)
        return response

    @staticmethod
    def get_test_by_jql(*, jaxa_client, jql_query: str) -> dict:
        response = jaxa_client.xray_gql.tests.get_tests_by_jql(jql_query=jql_query)
        return response
