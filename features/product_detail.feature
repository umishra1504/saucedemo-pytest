Feature: Product Detail Page
  As a user
  I want to view product details and add items to cart from the detail page
  So that I can review product information before purchasing

  Background:
    Given I am logged in as a standard user
    And I am on the inventory page

  @product_detail @smoke
  Scenario: Open product detail page from inventory
    # TC-SCRUM-172-001: Open product detail page from inventory
    When I click on product "Sauce Labs Backpack" from the inventory
    Then I should be on the product detail page
    And the URL should contain "inventory-item.html"

  @product_detail @smoke
  Scenario: Verify product details and Add to Cart button are displayed
    # TC-SCRUM-172-002: Verify product details and Add to Cart button are displayed
    When I click on product "Sauce Labs Backpack" from the inventory
    Then I should see the product name "Sauce Labs Backpack"
    And I should see the product description
    And I should see the product price "$29.99"
    And I should see the "Add to cart" button

  @product_detail @regression
  Scenario: Add product to cart from detail page
    # TC-SCRUM-172-003: Add product to cart from detail page
    When I click on product "Sauce Labs Bolt T-Shirt" from the inventory
    And I add the product to cart from the detail page
    Then the cart badge should show 1 item
    And the "Remove" button should be displayed

  @product_detail @regression
  Scenario: Verify cart shows correct name and price for added detail-page item
    # TC-SCRUM-172-004: Verify cart shows correct name and price for added detail-page item
    When I click on product "Sauce Labs Bike Light" from the inventory
    And I add the product to cart from the detail page
    And I go to the cart page
    Then I should see "Sauce Labs Bike Light" in the cart
    And the cart item price should be "$9.99"

  @product_detail @smoke
  Scenario: Return to inventory using back button
    # TC-SCRUM-172-005: Return to inventory using back button
    When I click on product "Sauce Labs Fleece Jacket" from the inventory
    And I click the back to products button
    Then I should be redirected to the inventory page
    And the URL should contain "inventory.html"

  @product_detail @regression
  Scenario: Preserve cart state after navigating back to inventory
    # TC-SCRUM-172-006: Preserve cart state after navigating back to inventory
    When I add product 0 to the cart
    And the cart badge should show 1 item
    And I click on product "Sauce Labs Bolt T-Shirt" from the inventory
    And I add the product to cart from the detail page
    And the cart badge should show 2 items
    And I click the back to products button
    Then I should be redirected to the inventory page
    And the cart badge should still show 2 items
