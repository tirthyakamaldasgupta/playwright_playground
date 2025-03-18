"""
Playwright Request Interception and Mocking Guide

This script demonstrates how to intercept and mock network requests using Playwright's `page.route()` method.
It includes:
- **What is Request Interception?**
- **How to Mock API Responses?**
- **Handling Multiple Routes**
- **Asserting Mocked Data**

# What is Request Interception?
Request interception allows Playwright to listen to network requests made by the browser and modify or block them before they reach the server.
This is useful for:
- Mocking API responses during testing
- Blocking certain requests (e.g., ads, analytics)
- Manipulating request headers

# How to Mock API Responses?
Mocking is done using the `page.route()` method, which allows us to intercept a request and fulfill it with a custom response.
This prevents actual network calls, ensuring tests run fast and reliably.

Example:
1. Use `page.route()` to match a URL pattern.
2. Inside the route handler, use `route.fulfill()` to return a mock response.
3. Verify the mocked response using assertions.

"""

import json
from playwright.sync_api import Page, Route


def test_multiple_interceptions(page: Page):
    """
    This test demonstrates how to intercept and mock multiple API requests.

    - Mocks the response for two API endpoints.
    - Verifies that the intercepted responses return the expected JSON.
    """

    # Handler for the first API
    def handle_first(route: Route):
        """
        This function intercepts an API request and returns a mocked response.

        - Status Code: 200 (OK)
        - Content Type: JSON
        - Response Body: {"message": "Mocked Response 1", "data": [1, 2, 3]}

        Parameters:
        route (Route): The intercepted route object.

        Behavior:
        - Instead of allowing the request to proceed, it directly returns a mock response.
        """
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"message": "Mocked Response 1", "data": [1, 2, 3]}),
        )

    # Handler for the second API
    def handle_second(route: Route):
        """
        This function intercepts an API request, fetches the real response, modifies it, and fulfills the request.

        - The intercepted request is first allowed to proceed using `route.fetch()`.
        - The JSON response is modified by adding an "email" field.
        - The modified response is sent back.

        Parameters:
        route (Route): The intercepted route object.

        Behavior:
        - The original response is fetched and converted to JSON.
        - The original key-value pair of the response is modified (Modification- `"email": "john.doe@gmail.com"`).
        - The modified response is returned instead of the original one.
        """
        response = route.fetch()
        json_response = response.json()
        json_response["email"] = "john.doe@gmail.com"

        route.fulfill(response=response, json=json_response)

    # Intercept and mock responses for two different API endpoints
    page.route("https://jsonplaceholder.typicode.com/posts/1", handle_first)
    page.route("https://jsonplaceholder.typicode.com/users/1", handle_second)

    # Navigate and verify first API response
    page.goto("https://jsonplaceholder.typicode.com/posts/1")
    content1 = json.loads(page.locator("body").inner_text())
    assert content1["message"] == "Mocked Response 1"
    assert content1["data"] == [1, 2, 3]

    # Navigate and verify second API response
    page.goto("https://jsonplaceholder.typicode.com/users/1")
    content2 = json.loads(page.locator("body").inner_text())
    assert content2["email"] == "john.doe@gmail.com"


"""
# Key Takeaways:
- `page.route(url, handler)` is used to intercept requests.
- `route.fulfill()` sends back a mocked response.
- Multiple routes can be intercepted and handled independently.
- This approach ensures tests are **fast, isolated, and reliable** without depending on external APIs.
"""
