@login
Feature: Login
  As a user of SauceDemo
  I want to log in with valid credentials
  So that I can access the product inventory

  @smoke
  Scenario: Successful login with standard user
    Given I am on the login page
    When I enter username "standard_user" and password "secret_sauce"
    And I click the login button
    Then I should be redirected to the inventory page

  Scenario: Login with invalid password
    Given I am on the login page
    When I enter username "standard_user" and password "wrong_password"
    And I click the login button
    Then I should see an error message containing "Username and password do not match"

  Scenario: Login with locked out user
    Given I am on the login page
    When I enter username "locked_out_user" and password "secret_sauce"
    And I click the login button
    Then I should see an error message containing "Sorry, this user has been locked out"

  Scenario: Login with empty credentials
    Given I am on the login page
    When I enter username "" and password ""
    And I click the login button
    Then I should see an error message containing "Username is required"
