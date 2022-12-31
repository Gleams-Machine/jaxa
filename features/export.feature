Feature: Test execution details exporting using Jira/Xray API

  @export
  Scenario Outline: Search for Test
    Given we use the JAXA client
    When we search using JQL <query>
    Then search results are returned

  Examples: JQL queries
    | query       |
    | type = TEST |
    | type = TEST And project = QA-Demo |
    | type = TEST And project = QA-Demo And testType = Cucumber |
    | type = TEST And project = QA-Demo And testType = Generic |
    | type = TEST And project = QA-Demo And testType = Manual |



"""
From a Testplan
Get all tests
For each test find all test executions
And Test runs


"""
