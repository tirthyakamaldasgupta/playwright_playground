"""
Advanced File Uploader Script

This script uses Playwright to automate the process of uploading a PDF file to the "I Love PDF" website.
It demonstrates handling complex file upload mechanisms on web pages that require interaction with the file chooser dialog, rather than just setting the file input element.

This script uses Playwright to automate the process of uploading a PDF file to the "I Love PDF" website.

Steps performed by the script:
1. Launches a Chromium browser instance in non-headless mode.
2. Opens a new browser page.
3. Navigates to the "I Love PDF" PDF to Word conversion page.
4. Waits for the file chooser dialog to appear after clicking the "Select PDF file" button.
5. Selects the specified PDF file ("OD222743347135959000.pdf") for upload.
6. Closes the browser.

Dependencies:
- playwright

Usage:
- Ensure that Playwright is installed and properly set up in your environment.
- Replace "OD222743347135959000.pdf" with the path to the PDF file you want to upload.
"""

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.ilovepdf.com/pdf_to_word")

    with page.expect_file_chooser() as fc_info:
        page.click("span:text('Select PDF file')")

    file_chooser = fc_info.value

    file_chooser.set_files("OD222743347135959000.pdf")

    browser.close()
