import re
from playwright.sync_api import Page, expect
import pytest


@pytest.fixture(scope="session")
def browser(playwright):
    """
    Fixture to launch a Chromium browser instance for the test session.
    Overrides the default browser fixture provided by Playwright.
    Args:
        playwright (Playwright): The Playwright instance.
    Yields:
        Browser: The launched Chromium browser instance.
    The browser is launched in non-headless mode and will be closed after the test session.
    """
    browser = playwright.chromium.launch(headless=False)

    yield browser

    browser.close()


@pytest.fixture(scope="function", autouse=True)
def go_to_url(page: Page):
    """
    Fixture to navigate to a specified URL before each test and perform cleanup after the test.
    This fixture is automatically used (autouse=True) for each test function within the scope.
    It navigates to "https://playwright.dev/" before the test runs and prints a message.
    After the test completes, it yields control back and prints another message.
    Args:
        page (Page): The Playwright page object used to interact with the browser.
    """
    page.goto("https://playwright.dev/")

    yield


@pytest.fixture(scope="function", autouse=True)
def expect_page_to_have_properties(page: Page, go_to_url):
    """
    A pytest fixture that runs before and after each test function to check if the page has the expected properties.
    This fixture is automatically used by all test functions due to `autouse=True`.
    Dependencies:
    - `page`: An instance of the Playwright `Page` object.
    - `go_to_url`: Another fixture that navigates to a specific URL before this fixture runs.
    Execution Order:
    1. The `go_to_url` fixture runs first to navigate to the desired URL.
    2. This fixture runs and checks if the page title contains the substring "Playwright".
    3. The test function executes.
    4. After the test function completes, the code after `yield` runs, printing "after the test runs".
    """
    expect(page).to_have_title(re.compile("Playwright"))

    yield


def test_has_title(page: Page):
    """
    Test to verify that the page title contains the substring "Playwright".

    This is a basic test using pre-available fixtures provided by pytest-playwright.
    """
    expect(
        page.locator("//div[@role='region']/following-sibling::div/header/div/h1/span")
    ).to_have_text(re.compile("Playwright"))
