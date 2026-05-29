# Test Suite: Product Detail Page with Cart Persistence (SCRUM-176)

## Overview
Automated test suite for validating product detail page functionality and cart persistence across navigation flows.

**Jira Story**: [SCRUM-176](https://umishra-1504.atlassian.net/browse/SCRUM-176)  
**Test Documentation**: [Confluence Test Cases](https://umishra-1504.atlassian.net/wiki/spaces/SD/pages/37552129/Test+Cases+Product+detail+page+from+inventory+with+cart+persistence+SCRUM-176)

## Feature Description
Users can click any product in the inventory to open a product detail page. The detail page shows the product's name, description, price, and an Add to Cart button. Products added from the detail page must appear in the cart with the correct name and price. Using the back button should return the user to the inventory page without losing cart state.

## Test Files Created

### 1. `tests/test_product_detail_cart_persistence.py`
Main test suite with all automated test cases for product detail page and cart persistence.

### 2. `pages/product_detail_page.py`
Page Object Model for the product detail page, providing methods to interact with product details, add/remove from cart, and navigate.

### 3. Updated Files
- `pages/cart_page.py` - Added `get_all_cart_item_names()` and `get_item_price_by_name()` methods
- `pages/inventory_page.py` - Added `get_all_product_names()` and `click_product_by_name()` methods

## Test Cases Automated

- [x] **TC-FP-001**: Open a product detail page from the inventory list
- [x] **TC-FP-002**: Verify product details and Add to Cart button render on the detail page
- [x] **TC-FP-003**: Add a product from the detail page to the cart
- [x] **TC-FP-004**: Verify cart displays correct product name and price after adding from detail page
- [x] **TC-FP-005**: Use browser back button to return to inventory page
- [x] **TC-FP-006**: Preserve cart state after returning to inventory using back button
- [x] **TC-FP-007**: Open detail page for the first and last visible inventory items
- [x] **TC-FP-008**: Add the same product from detail page more than once
- [x] **TC-FP-009**: Prevent cart from showing incorrect product data after navigation
- [x] **TC-FP-010**: Back navigation does not clear cart when the inventory page is refreshed

## Running the Tests

### Run all tests in the suite:
```bash
pytest tests/test_product_detail_cart_persistence.py -v
```

### Run a specific test:
```bash
pytest tests/test_product_detail_cart_persistence.py::TestProductDetailCartPersistence::test_open_product_detail_from_inventory -v
```

### Run with HTML report:
```bash
pytest tests/test_product_detail_cart_persistence.py --html=reports/product_detail_tests.html --self-contained-html
```

### Run in headless mode:
```bash
pytest tests/test_product_detail_cart_persistence.py --headed
```

## Test Coverage Summary

| Category | Test Cases | Automated |
|----------|-----------|-----------|
| Navigation | 3 | ✅ 3 |
| Product Display | 2 | ✅ 2 |
| Cart Operations | 3 | ✅ 3 |
| Data Integrity | 2 | ✅ 2 |
| **Total** | **10** | **✅ 10** |

## Dependencies

- `pytest` - Testing framework
- `playwright` - Browser automation
- Existing page objects: `LoginPage`, `InventoryPage`, `CartPage`
- New page object: `ProductDetailPage`

## Test Data

Tests use the standard SauceDemo test user:
- **Username**: `standard_user`
- **Password**: `secret_sauce`

## Notes

- All tests include automatic login setup via fixture
- Tests follow existing project conventions and patterns
- Page Object Model pattern is used for maintainability
- Each test is independent and can run in isolation
- Cart state is validated across navigation boundaries
- Tests verify both UI state and URL navigation

## CI/CD Integration

These tests can be integrated into the existing CI/CD pipeline:

```yaml
- name: Run Product Detail Tests
  run: pytest tests/test_product_detail_cart_persistence.py -v --junit-xml=reports/junit.xml
```

## Maintenance

- Update `ProductDetailPage` locators if the application changes
- Add new test cases to the test class following the existing pattern
- Keep test case IDs (TC-FP-XXX) in sync with Confluence documentation
