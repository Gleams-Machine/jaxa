Feature: TestPlan creation using Jira/Xray API

  @testplan
  Scenario: Create an empty TestPlan
    Given we use the JAXA client
    When we opt to create an empty TestPlan
    Then a TestPlan is created with no tests

  @testplan
  @tests
  Scenario: Create a TestPlan with tests
     Given we use the JAXA client
     When we opt to create a TestPlan with tests
     | test_type | test_summary                     |
     | cucumber  | Test: JAXA created Cucumber Test |
     | generic   | Test: JAXA created Generic Test  |
     | manual    | Test: JAXA created Manual Test   |
     Then a TestPlan is created with the tests
