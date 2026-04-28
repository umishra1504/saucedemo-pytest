@inventory
Feature: Inventory
  As a logged-in user
  I want to browse and interact with products
  So that I can find items to purchase

  Background:
    Given I am logged in as a standard user

  @smoke
  Scenario: View products on inventory page
    Then I should see the inventory page title "Products"
    And I should see 6 products listed

  Scenario: Sort products by name Z to A
    When I sort products by "za"
    Then the first product should be "Test.allTheThings() T-Shirt (Red)"

  Scenario: Sort products by price low to high
    When I sort products by "lohi"
    Then the first product should be "Sauce Labs Onesie"

  @smoke
  Scenario: Add a product to cart
    When I add product 0 to the cart
    Then the cart badge should show 1 item
