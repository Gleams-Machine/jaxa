Feature: TestSet querying using Jira/Xray API

  @testsets
  Scenario Outline: Search for TestSet
    Given we use the JAXA client
    When we opt to create an empty TestSet with summary <summary>
    And we search for TestSet using JQL <query>
    Then TestSet search results are returned
    And TestSet query result contains expected TestSet

  Examples: JQL queries
    | summary        | query                                                  |
    | TestSet: {uid} | type = "Test Set" And project = "QD" ORDER BY key DESC |
