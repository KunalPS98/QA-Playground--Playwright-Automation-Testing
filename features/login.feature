Feature: Login
  As a returning customer
  I want to log in with my account
  So that I can access my cart, orders, and profile

  Scenario: Logging in with valid credentials
    Given I am on the login page
    When I log in with a valid sample account
    Then I should be logged in

  Scenario: Logging in with an invalid password
    Given I am on the login page
    When I log in with the wrong password
    Then I should see an "Invalid email or password." error
