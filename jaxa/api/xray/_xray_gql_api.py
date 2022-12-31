"""
Jira XRay GQL API
"""

from ...api.graphql._gql_client import GQLAPIClient
from ...api.xray._xray_categories import GQLTests, GQLTestPlan, GQLTestExecution, GQLTestRun, GQLTestSets, GQLTestStatus


class XRayGraphQLAPI(GQLAPIClient):
    """XRay GraphQL API"""

    @property
    def tests(self):
        """
        Perform the actual call and return response
        """
        return GQLTests(self)

    @property
    def test_plan(self):
        """
        Perform the actual call and return response
        """
        return GQLTestPlan(self)

    @property
    def test_executions(self):
        """
        Perform the actual call and return response
        """
        return GQLTestExecution(self)

    @property
    def test_runs(self):
        """
        Perform the actual call and return response
        """
        return GQLTestRun(self)

    @property
    def test_sets(self):
        """
        Perform the actual call and return response
        """
        return GQLTestSets(self)

    @property
    def test_statuses(self):
        """

        """
        return GQLTestStatus(self)
