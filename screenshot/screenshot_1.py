import os
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    page = context.new_page()

    page.goto("https://demo.automationtesting.in/FileUpload.html")

    page.screenshot(path=os.path.join(os.getcwd(), "screenshot", "screenshot.png"), full_page=True)

    browser.close()
