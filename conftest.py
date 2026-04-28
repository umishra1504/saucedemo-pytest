import pytest
from utils.logger import get_logger
from utils.config import BASE_URL

log = get_logger("conftest")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": BASE_URL,
        "viewport": {"width": 1280, "height": 720},
    }


def pytest_configure(config):
    log.info("Test session starting")
    log.info(f"Base URL: {BASE_URL}")


def pytest_sessionfinish(session, exitstatus):
    log.info(f"Test session finished with exit status: {exitstatus}")
