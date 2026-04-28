# SauceDemo Pytest BDD Framework

Automated test framework for [SauceDemo](https://www.saucedemo.com) using **Pytest + Playwright + pytest-bdd**.

## Tech Stack

- **Python 3.11+**
- **Playwright** — Browser automation
- **pytest-bdd** — BDD with Gherkin feature files
- **Page Object Model** — Clean separation of page logic
- **uv** — Fast Python package manager

## Setup

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Install Playwright browsers
uv run playwright install chromium
```

## Configuration

Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://www.saucedemo.com` | Target application URL |
| `HEADLESS` | `true` | Run browser in headless mode |
| `SLOW_MO` | `0` | Slow down actions by ms (for debugging) |

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with headed browser
uv run pytest --headed

# Run specific feature
uv run pytest -m login
uv run pytest -m inventory
uv run pytest -m cart

# Run smoke tests only
uv run pytest -m smoke

# Generate Playwright HTML report
uv run pytest --output=reports/

# Run with tracing (for debugging)
uv run pytest --tracing=on
```

## Project Structure

```
├── features/          # Gherkin .feature files
├── step_defs/         # Step definitions (test_*.py)
├── pages/             # Page Object Model classes
├── utils/             # Config, logging utilities
├── reports/           # Test reports (gitignored)
├── logs/              # Log files (gitignored)
├── conftest.py        # Root pytest fixtures
└── pyproject.toml     # Project config & dependencies
```

## Writing New Tests

1. Create a `.feature` file in `features/`
2. Create a page object in `pages/` (if new page)
3. Write step definitions in `step_defs/test_<feature>.py`
4. Use `scenarios("../features/<name>.feature")` to link them
