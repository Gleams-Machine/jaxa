Feature: Test creation using Jira/Xray API

  @tests
  Scenario Outline: Create a Test
    Given we use the JAXA client
    When we opt to create a <test_type> Test with default summary
    Then a <test_type> Test is created

  Examples: TestTypes
    | test_type |
    | Cucumber  |
    | Generic   |
    | Manual    |
