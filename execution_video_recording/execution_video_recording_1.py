import os
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(record_video_dir=os.path.join(os.getcwd(), "execution_video_recording", "videos"))

    page = context.new_page()

    page.goto("https://demo.automationtesting.in/FileUpload.html")

    browser.close()
