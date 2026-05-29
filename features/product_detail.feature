@product_detail
Feature: Product Detail Page
  As a logged-in user
  I want to view product details and add items to cart from the detail page
  So that I can make informed purchase decisions

  Background:
    Given I am logged in as a standard user
    And I am on the inventory page

  @smoke @SCRUM-172
  Scenario: Open product detail page from inventory
    # TC-FP-001: Open product detail page from inventory
    When I click on product "Sauce Labs Backpack"
    Then I should be on the product detail page
    And the URL should contain "inventory-item.html"

  @smoke @SCRUM-172
  Scenario: Verify product details and Add to Cart button are displayed
    # TC-FP-002: Verify product details and Add to Cart button are displayed
    When I click on product "Sauce Labs Backpack"
    Then I should see the product name "Sauce Labs Backpack"
    And I should see a product description
    And I should see a product price
    And I should see an "Add to cart" button

  @SCRUM-172
  Scenario: Add product to cart from detail page
    # TC-FP-003: Add product to cart from detail page
    When I click on product "Sauce Labs Bike Light"
    And I add the product to cart from the detail page
    Then the cart badge should show 1 item
    And the "Remove" button should be visible

  @SCRUM-172
  Scenario: Verify cart shows correct name and price for added detail-page item
    # TC-FP-004: Verify cart shows correct name and price for added detail-page item
    Given I click on product "Sauce Labs Bolt T-Shirt"
    And I add the product to cart from the detail page
    When I navigate to the cart page
    Then I should see 1 item in the cart
    And the cart should contain product "Sauce Labs Bolt T-Shirt"
    And the cart item should have price "$15.99"

  @smoke @SCRUM-172
  Scenario: Return to inventory using back button
    # TC-FP-005: Return to inventory using back button
    When I click on product "Sauce Labs Fleece Jacket"
    And I click the back button
    Then I should be redirected to the inventory page
    And I should see 6 products listed

  @SCRUM-172
  Scenario: Preserve cart state after navigating back to inventory
    # TC-FP-006: Preserve cart state after navigating back to inventory
    When I add product 0 to the cart from inventory
    And I click on product "Sauce Labs Bike Light"
    And I add the product to cart from the detail page
    And I click the back button
    Then I should be redirected to the inventory page
    And the cart badge should show 2 items
