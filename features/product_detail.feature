Feature: Product Detail Page with Add to Cart Functionality
  As a SauceDemo user
  I want to view product details and add items to the cart
  So that I can manage purchases from the inventory and detail pages

  Scenario: Open a product detail page from the inventory list
    Given I am logged in as a standard user
    When I open product 0 from the inventory list
    Then I should be on the product detail page for product 0

  Scenario: Verify product detail page displays complete product information
    Given I am logged in as a standard user
    When I open product 0 from the inventory list
    Then I should see the selected product name
    And I should see the selected product description
    And I should see the selected product price
    And I should see the add to cart button

  Scenario: Add a product from the detail page to the cart
    Given I am logged in as a standard user
    When I open product 0 from the inventory list
    And I add the product to the cart from the detail page
    And I open the cart page
    Then I should see 1 item in the cart
    And the cart should contain the selected product name
    And the cart should contain the selected product price

  Scenario: Use back button to return to inventory page
    Given I am logged in as a standard user
    When I open product 0 from the inventory list
    And I click back on the detail page
    Then I should be redirected to the inventory page

  Scenario: Preserve cart state when navigating from inventory to product detail and back
    Given I am logged in as a standard user
    When I add product 0 to the cart
    And I open product 1 from the inventory list
    And I click back on the detail page
    Then the cart badge should show 1 item

  Scenario: Open detail page for the first and last product in the inventory list
    Given I am logged in as a standard user
    When I open product 0 from the inventory list
    Then I should be on the product detail page for product 0
    When I click back on the detail page
    And I open product last from the inventory list
    Then I should be on the product detail page for product last

  Scenario: Verify product detail page renders correctly for long product name and description
    Given I am logged in as a standard user
    When I open product 0 from the inventory list
    Then the selected product details should render without layout issues

  Scenario: Verify price is displayed correctly for decimal and zero values
    Given I am logged in as a standard user
    When I open product 0 from the inventory list
    Then the selected product price should be displayed in currency format

  Scenario: Preserve cart state across repeated navigation between inventory and detail pages
    Given I am logged in as a standard user
    When I add product 0 to the cart
    And I open product 1 from the inventory list
    And I click back on the detail page
    And I open product 2 from the inventory list
    And I click back on the detail page
    Then the cart badge should show 1 item

  Scenario: Handle direct access to an invalid product detail route
    Given I am logged in as a standard user
    When I navigate to an invalid product detail route
    Then I should see an invalid product error state

  Scenario: Prevent add-to-cart action when product data is unavailable
    Given I am logged in as a standard user
    When I open a product detail page with unavailable data
    Then the add to cart action should be unavailable

  Scenario: Maintain cart integrity against tampered product data
    Given I am logged in as a standard user
    When I attempt to tamper with product detail data
    Then the cart should not accept tampered product data
