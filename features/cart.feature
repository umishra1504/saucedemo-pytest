@cart
Feature: Cart
  As a logged-in user
  I want to manage items in my cart
  So that I can prepare my order

  Background:
    Given I am logged in as a standard user

  @smoke
  Scenario: Add item and view in cart
    When I add product 0 to the cart
    And I go to the cart page
    Then I should see 1 item in the cart

  Scenario: Remove item from cart
    When I add product 0 to the cart
    And I go to the cart page
    And I remove item 0 from the cart
    Then I should see 0 items in the cart

  Scenario: Continue shopping from cart
    When I add product 0 to the cart
    And I go to the cart page
    And I click continue shopping
    Then I should be redirected to the inventory page
