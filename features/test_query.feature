Feature: Test querying using Jira/Xray API

  Background: Create tests for searching
    Given we use the JAXA client
    When we opt to create a Cucumber Test
    And we opt to create a Manual Test
    And we opt to create a Generic Test

  @tests
  Scenario Outline: Search for Test
    Given we use the JAXA client
    When we search for Tests using JQL <query>
    Then search results are returned

  Examples: JQL queries
    | query       |
    | type = TEST |
    | type = TEST And project = QA-Demo |
    | type = TEST And project = QA-Demo And testType = Cucumber |
    | type = TEST And project = QA-Demo And testType = Generic |
    | type = TEST And project = QA-Demo And testType = Manual |
