Feature: TestExecution creation using Jira/Xray API

  @testexecution
  Scenario Outline: Record a TestExecution result
    Given we use the JAXA client
    When we opt to create an empty TestPlan
    And we opt to create a <test_type> Test with default summary
    And we opt to create a TestExecution
    And we get TestRuns
    And we add a TestExecution to a TestPlan
    And we set the TestRun status to Passed

  Examples: TestTypes
    | test_type |
    | Cucumber  |
    | Generic   |
    | Manual    |
