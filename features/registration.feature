Feature: Registration
  As a new visitor
  I want to create an account
  So that I can shop on QA Playground

  Scenario: Registering with valid, unique details
    Given I am on the registration page
    When I register with a new, unique account
    Then I should be logged in as that new account
