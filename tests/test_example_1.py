import re
from playwright.sync_api import Page, expect


def test_has_title(page: Page):
    """
    Test to verify that the page title contains the substring "Playwright".

    This is a basic test using pre-available fixtures provided by pytest-playwright.
    """
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))
