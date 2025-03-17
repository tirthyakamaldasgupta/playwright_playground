import os
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    page = context.new_page()

    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page.goto("https://demo.automationtesting.in/FileUpload.html")

    page.screenshot(path=os.path.join(os.getcwd(), "tracing", "screenshot.png"), full_page=True)

    context.tracing.stop(path=os.path.join(os.getcwd(), "tracing", "trace.zip"))

    browser.close()
