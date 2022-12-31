
class TestSetActions:
    @staticmethod
    def create_empty_testset(*, jaxa_client, summary: str,  project_key: str):
        response = jaxa_client.xray_gql.test_sets.create_empty_testset(
            project_key=project_key,
            summary=summary,
        )
        print(response)
        return response

    @staticmethod
    def create_testset_with_tests(*, jaxa_client, summary: str, project_key: str, test_ids: list):
        response = jaxa_client.xray_gql.test_sets.create_testset_with_tests(
            project_key=project_key,
            summary=summary,
            test_ids=test_ids
        )
        print(response)
        return response

    @staticmethod
    def get_tests_in_testset(*, jaxa_client, testset_id: str):
        response = jaxa_client.xray_gql.test_sets.get_tests_in_testset(
            testset_id=testset_id
        )
        print(response)
        return response

    @staticmethod
    def add_tests_to_testset(*, jaxa_client, testset_id: str, test_ids: list):
        response = jaxa_client.xray_gql.test_sets.add_tests_to_testset(
            testset_id=testset_id,
            test_ids=test_ids
        )
        print(response)
        return response

    @staticmethod
    def remove_tests_from_testset(*, jaxa_client, testset_id: str, test_ids: list):
        response = jaxa_client.xray_gql.test_sets.remove_tests_from_testset(
            testset_id=testset_id,
            test_ids=test_ids
        )
        print(response)
        return response

    @staticmethod
    def get_testsets_by_jql(*, jaxa_client, jql: str):
        response = jaxa_client.xray_gql.test_sets.get_testsets_by_jql(jql=jql)
        print(response)
        return response
