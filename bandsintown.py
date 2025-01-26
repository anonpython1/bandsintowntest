from playwright.sync_api import sync_playwright

def bandsintown_scraper():
    with sync_playwright() as p:
        # Launch browser (set headless=False to see the browser)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto("https://www.bandsintown.com/a/12895856-billie-eilish?came_from=251", wait_until="domcontentloaded")
            # class name for show More details   (OsDXzJEUtjxbMlCnPMsj)
            page.wait_for_selector(".OsDXzJEUtjxbMlCnPMsj")
            page.click(".OsDXzJEUtjxbMlCnPMsj")
            # To see the button is clicked or not.
            page.wait_for_timeout(9000)
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    bandsintown_scraper()
