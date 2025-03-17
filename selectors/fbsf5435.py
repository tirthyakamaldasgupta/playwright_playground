import os
from playwright.sync_api import sync_playwright, Playwright

def run(p: Playwright):
        browser = p.chromium.launch(headless=False)

        context = browser.new_context()

        page = context.new_page()

        page.goto("https://demo.automationtesting.in/Register.html")

        page.locator("#section").screenshot(path=os.path.join(os.getcwd(), "selectors", "section-screenshot.png")) # id css selector
        page.locator("form#basicBootstrapForm").screenshot(path=os.path.join(os.getcwd(), "selectors", "basicBootstrapForm-screenshot.png")) # specific element id selector

        browser.close()


with sync_playwright() as p:
    run(p)
