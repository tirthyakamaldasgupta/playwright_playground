import pytest
from playwright.sync_api import Page, expect

# ==============================
# Dialog Handling Functions
# ==============================


def handle_dialog_accept(dialog):
    """Handles the dialog by clicking 'OK' or 'Accept'."""
    dialog.accept()


def handle_dialog_dismiss(dialog):
    """Handles the dialog by clicking 'Cancel' or dismissing it."""
    dialog.dismiss()


def handle_dialog_accept_with_message(dialog):
    """Handles the prompt dialog by providing an input message and clicking 'OK'."""
    dialog.accept("Accepted")


def handle_dialog_dismiss_with_message(dialog):
    """Handles the prompt dialog by dismissing it."""
    dialog.dismiss()


# ==============================
# Pytest Fixture: Navigate to URL Before Tests
# ==============================


@pytest.fixture(scope="function", autouse=True)
def navigate_to_url(page: Page):
    """
    This fixture automatically navigates to the test page before each test case.
    The page URL contains JavaScript alerts, confirmations, and prompt dialogs.
    """
    page.goto("https://testpages.eviltester.com/styled/alerts/alert-test.html")
    yield


# ==============================
# Test Case 1: Handling an Alert Dialog
# ==============================


def test_closing_alert(page: Page):
    """
    This test:
    1. Clicks the 'Show Alert Box' button.
    2. Listens for the alert and accepts it.
    3. Verifies that the page reflects the alert was handled.
    """

    # Attach an event listener to handle the alert dialog.
    page.on("dialog", handle_dialog_accept)

    # Trigger the alert by clicking the button
    page.locator("#alertexamples").click()

    # Assert that the alert was handled successfully
    expect(page.locator("#alertexplanation")).to_have_text(
        "You triggered and handled the alert dialog"
    )


# ==============================
# Test Case 2: Handling a Confirmation Dialog
# ==============================


def test_closing_confirm(page: Page):
    """
    This test:
    1. Clicks the 'Show Confirm Box' button.
    2. Accepts the confirmation dialog and verifies the result.
    3. Dismisses the confirmation dialog and verifies the result.
    """

    # Step 1: Accept the confirmation dialog
    page.on("dialog", handle_dialog_accept)
    page.locator("#confirmexample").click()

    # Verify that the confirmation returned "true"
    expect(page.locator("#confirmreturn")).to_have_text("true")
    expect(page.locator("#confirmexplanation")).to_have_text(
        "You clicked OK, confirm returned true."
    )

    # Remove the previous event listener
    page.remove_listener("dialog", handle_dialog_accept)

    # Step 2: Dismiss the confirmation dialog
    page.on("dialog", handle_dialog_dismiss)
    page.locator("#confirmexample").click()

    # Verify that the confirmation returned "false"
    expect(page.locator("#confirmreturn")).to_have_text("false")
    expect(page.locator("#confirmexplanation")).to_have_text(
        "You clicked Cancel, confirm returned false."
    )


# ==============================
# Test Case 3: Handling a Prompt Dialog with Input
# ==============================


def test_closing_confirm_message(page: Page):
    """
    This test:
    1. Clicks the 'Show Prompt Box' button.
    2. Enters a message and accepts the prompt.
    3. Verifies that the page reflects the entered message.
    4. Dismisses the prompt without entering a message and verifies the result.
    """

    # Step 1: Accept the prompt with a custom message
    page.on("dialog", handle_dialog_accept_with_message)
    page.locator("#promptexample").click()

    # Verify that the page displays the entered message
    expect(page.locator("#promptreturn")).to_have_text("Accepted")
    expect(page.locator("#promptexplanation")).to_have_text(
        "You clicked OK. 'prompt' returned Accepted"
    )

    # Remove the previous event listener
    page.remove_listener("dialog", handle_dialog_accept_with_message)

    # Step 2: Dismiss the prompt without entering a message
    page.on("dialog", handle_dialog_dismiss_with_message)
    page.locator("#promptexample").click()

    # Verify that the prompt was dismissed
    expect(page.locator("#promptexplanation")).to_have_text(
        "You clicked Cancel. 'prompt' returned null"
    )
