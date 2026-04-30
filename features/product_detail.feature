@product_detail
Feature: Product detail page with add-to-cart functionality
  As a logged-in user
  I want to open a product detail page, add products from the detail view, and return to inventory without losing cart state
  So that I can review product information and manage my cart accurately

  Background:
    Given I am logged in as a standard user

  Scenario: Navigate from inventory to selected product detail page
    When I open the first product from the inventory
    Then I should be on the product detail page for "Sauce Labs Backpack"

  Scenario: Open product detail page via direct navigation to ensure correct product loads
    When I directly open product detail page for "0"
    Then I should be on the product detail page for "Sauce Labs Backpack"

  Scenario: Verify detail page renders correct product information and add-to-cart button
    When I directly open product detail page for "0"
    Then I should see the product detail information for "Sauce Labs Backpack"
    And I should see the Add to Cart button on the product detail page

  Scenario: Validate rendering of long product text and price formatting on detail page
    When I directly open product detail page for "4"
    Then I should see the product detail information for "Sauce Labs Fleece Jacket"
    And I should see a price formatted as "$49.99" on the product detail page

  Scenario: Add product to cart from product detail page
    When I directly open product detail page for "0"
    And I add the product to the cart from the detail page
    Then the cart badge should show 1 item on the product detail page
    And the product should be marked as removed on the product detail page

  Scenario: Add the same product to cart when cart already contains items
    When I add the first inventory product to the cart
    And I directly open product detail page for "1"
    And I add the product to the cart from the detail page
    Then the cart badge should show 2 items on the product detail page

  Scenario: Verify cart count updates after adding item from detail page
    When I directly open product detail page for "0"
    And I add the product to the cart from the detail page
    Then the cart badge should show 1 item on the product detail page

  Scenario: Return to inventory using back button while preserving cart state
    When I directly open product detail page for "0"
    And I add the product to the cart from the detail page
    And I go back to the inventory from the product detail page
    Then I should be on the inventory page
    And the cart badge should still show 1 item on the inventory page

  Scenario: Use browser back navigation after adding an item and confirm cart persists
    When I directly open product detail page for "0"
    And I add the product to the cart from the detail page
    And I use browser back navigation
    Then I should be on the inventory page
    And the cart badge should still show 1 item on the inventory page

  Scenario: Attempt to open an invalid or non-existent product detail page
    When I directly open product detail page for "999"
    Then I should see an error or an empty product detail state

  Scenario: Verify Add to Cart is unavailable or no-op while product data is not loaded
    When I directly open an invalid product detail page from the address bar
    Then I should see an error or an empty product detail state

  Scenario: Prevent cart updates from tampered product identifiers or unauthorized item injection
    When I directly open product detail page for "0"
    And I try to tamper with the product identifier in the browser
    Then cart state should remain unchanged
