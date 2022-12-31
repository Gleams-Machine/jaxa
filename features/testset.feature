Feature: TestSet maintenance using Jira/Xray API

  @testsets
  Scenario: Create an empty TestSet
    Given we use the JAXA client
    When we opt to create an empty TestSet
    Then a TestSet contains no tests

  @testsets
  @tests
  Scenario: Create a TestSet with tests
     Given we use the JAXA client
     When we opt to create a TestSet with tests
     | test_type | test_summary                     |
     | Cucumber  | Test: JAXA created Cucumber Test |
     | Generic   | Test: JAXA created Generic Test  |
     | Manual    | Test: JAXA created Manual Test   |
     Then the TestSet contains the tests

  @testsets
  @tests
  Scenario: Add Tests to a TestSet
     Given we use the JAXA client
     When we opt to create an empty TestSet
     And add a Test into the TestSet
     | test_type | test_summary                     |
     | Cucumber  | Test: JAXA created Cucumber Test |
     | Generic   | Test: JAXA created Generic Test  |
     | Manual    | Test: JAXA created Manual Test   |
     Then the TestSet contains the tests

  @testsets
  @tests
  Scenario: Remove Tests from a TestSet
     Given we use the JAXA client
     When we opt to create a TestSet with tests
     | test_type | test_summary                     |
     | Cucumber  | Test: JAXA created Cucumber Test |
     | Generic   | Test: JAXA created Generic Test  |
     | Manual    | Test: JAXA created Manual Test   |
     And remove a Test from the TestSet
     | test_type | test_summary                     |
     | Generic   | Test: JAXA created Generic Test  |
     Then the TestSet contains the tests
