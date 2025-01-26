from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import re
from unidecode import unidecode


def bandsintown_scraper():
    with sync_playwright() as p:
        # Launch browser (set headless=False to see the browser)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto("https://www.bandsintown.com/a/12895856-billie-eilish?came_from=251", wait_until="domcontentloaded")
            # class name for show More details (OsDXzJEUtjxbMlCnPMsj)
            page.wait_for_selector(".OsDXzJEUtjxbMlCnPMsj")
            page.click(".OsDXzJEUtjxbMlCnPMsj")
            all_events = page.query_selector_all(".TNgS3aApp6XIXOIqyEGQ")
            artist = page.query_selector(".sKZg4aYIueqDu5cAfZ_q").inner_text()
            event_list = []
            for event in all_events:
                month = event.query_selector(".jnX2IOn9AGg9SfWK4eCL").inner_text()
                date = event.query_selector(".vLfdQ0HSBUy47Eujeqkk").inner_text()
                venu = event.query_selector(".TYzA8d85IfvLeyChcYJj").inner_text()
                decoded_text = venu.encode("utf-8").decode("unicode_escape")
                decoded_venu = unidecode(decoded_text)

                location = event.query_selector(".D9Nc3q2GrC4mEVUaPKoR").inner_text()
                state, country = location.split(",")
                decoded_text = state.encode("utf-8").decode("unicode_escape")
                decoded_state = unidecode(decoded_text)

                # Convert month and date to "YYYY-MM-DD" format
                event_date = datetime.strptime(f"{month} {date} 2025", "%b %d %Y").strftime("%Y-%m-%d")
                event_list.append({
                    "artist": artist,
                    "start_date": event_date,
                    "end_date": event_date,
                    "venue": decoded_venu,
                    "city/state": decoded_state.strip(),
                    "country": country.strip()
                })

            with open('events.json', 'w') as f:
                json.dump(event_list, f, indent=4)

        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    bandsintown_scraper()
