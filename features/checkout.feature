Feature: Checkout flow
  As a SauceDemo shopper
  I want to provide shipping information and complete my purchase
  So that I can verify order summary and validation behavior

  Scenario: Proceed to checkout after adding an item to the cart
    Given I am logged in as a standard user
    And I have an item in the cart
    When I go to the cart page
    And I proceed to checkout
    Then I should see the checkout information page

  Scenario: Enter valid shipping information in checkout form
    Given I am logged in as a standard user
    And I have an item in the cart
    When I go to the cart page
    And I proceed to checkout
    And I enter shipping information with first name "John", last name "Doe", and zip code "12345"
    Then the shipping fields should accept first name John, last name Doe, zip code 12345

  Scenario: View order summary with item total and tax before purchase
    Given I am logged in as a standard user
    And I have an item in the cart
    When I go to the cart page
    And I proceed to checkout
    And I enter shipping information with first name "John", last name "Doe", and zip code "12345"
    And I continue checkout
    Then I should see the checkout overview page
    And I should see item total and tax in the order summary

  Scenario: Complete purchase successfully with valid shipping details
    Given I am logged in as a standard user
    And I have an item in the cart
    When I go to the cart page
    And I proceed to checkout
    And I enter shipping information with first name "John", last name "Doe", and zip code "12345"
    And I continue checkout
    And I finish the purchase
    Then I should see the order complete page

  Scenario Outline: Verify checkout form accepts boundary-length shipping names
    Given I am logged in as a standard user
    And I have an item in the cart
    When I go to the cart page
    And I proceed to checkout
    And I enter shipping information with first name "<first_name>", last name "<last_name>", and zip code "12345"
    Then the shipping fields should accept first name <first_name>, last name <last_name>, zip code 12345

    Examples:
      | first_name | last_name |
      | A          | B         |
      | Alexander  | Hamilton  |

  Scenario: Verify order summary updates consistently for a cart with multiple items
    Given I am logged in as a standard user
    And I have multiple items in the cart
    When I go to the cart page
    And I proceed to checkout
    And I enter shipping information with first name "John", last name "Doe", and zip code "12345"
    And I continue checkout
    Then I should see the checkout overview page
    And I should see item total and tax in the order summary

  Scenario Outline: Prevent checkout submission when shipping fields are empty
    Given I am logged in as a standard user
    And I have an item in the cart
    When I go to the cart page
    And I proceed to checkout
    And I enter shipping information with first name "<first_name>", last name "<last_name>", and zip code "<zip_code>"
    And I continue checkout
    Then I should see a validation error

    Examples:
      | first_name | last_name | zip_code |
      |            | Doe       | 12345    |
      | John       |           | 12345    |
      | John       | Doe       |          |
      |            |           |          |
