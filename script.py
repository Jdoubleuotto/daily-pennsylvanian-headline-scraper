"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor

import bs4
import requests
import loguru


# def scrape_data_point():
#     """
#     Scrapes the main headline from The Daily Pennsylvanian home page.

#     Returns:
#         str: The headline text if found, otherwise an empty string.
#     """
#     req = requests.get("https://www.thedp.com")
#     loguru.logger.info(f"Request URL: {req.url}")
#     loguru.logger.info(f"Request status code: {req.status_code}")

#     if req.ok:
#         soup = bs4.BeautifulSoup(req.text, "html.parser")
#         target_element = soup.find("a", class_="frontpage-link")
#         data_point = "" if target_element is None else target_element.text
#         loguru.logger.info(f"Data point: {data_point}")
#         return data_point

def get_latest_crossword_url():
    response = requests.get(crosswords_page_url)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the URL of the latest crossword based on the HTML structure
        # This is a placeholder; you'll replace it with the actual selector
        latest_crossword_link = soup.find('h3', class_='standard-link')
        if crossword_link_tag and crossword_link_tag.a:
            crossword_url = crossword_link_tag.a['href']
            loguru.logger.info(f"Latest crossword URL: {crossword_url}")
            return crossword_url
        else:
            loguru.logger.info("Latest crossword URL not found.")
            return None

def get_latest_hints_across_down():
    response = requests.get(get_lastest_crossword_url())
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the clues for words going across
        crossword_clues = soup.find_all('div', class_='clueDiv', limit=10)
        crossword_clues_text = [clue.find('span', class_='clueText').text for clue in crossword_clues if clue.find('span', class_='clueText')]
        
        # Output the clues
        for i, clue in enumerate(crossword_clues_text, start=1):
            print(f"Across {i}: {clue}")


if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_data_point()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point is not None:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
