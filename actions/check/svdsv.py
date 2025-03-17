import os
import time
from playwright.sync_api import sync_playwright, Playwright

def run(p: Playwright):
        browser = p.chromium.launch(headless=False)

        context = browser.new_context()

        page = context.new_page()

        page.goto("https://demo.applitools.com")

        time.sleep(2)

        page.locator("input[type='checkbox']").check()

        time.sleep(2)

        browser.close()


with sync_playwright() as p:
    run(p)
