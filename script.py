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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

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

crosswords_page_url = "https://www.thedp.com/section/mini-crosswords"

# def get_latest_crossword_url():
#     response = requests.get(crosswords_page_url)
#     loguru.logger.info(f"Request URL: {response.url}")
#     loguru.logger.info(f"Request status code: {response.status_code}")
#     if response.ok:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         latest_crossword_link = soup.find('h3', class_='standard-link')
#         if latest_crossword_link and latest_crossword_link.a:
#             crossword_url = latest_crossword_link.a['href']
#             loguru.logger.info(f"Latest crossword URL: {crossword_url}")
#             return crossword_url
#         else:
#             loguru.logger.info("Latest crossword URL not found.")
#             return None


def scrape_data_point():
    # Set up the Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    
    # Set path to chromedriver as per your configuration
    webdriver_path = '/path/to/chromedriver'
    
    # Establish a session with the web page
    driver = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)
    
    # URL of the page you want to scrape
    url = 'https://www.thedp.com/article/2024/03/mini-crossword-03-15'
    
    # Open the page
    driver.get(url)
    
    # Wait for the dynamic content to load
    sleep(5)
    
    # Now that the page is fully dynamically loaded, we can start scraping
    clues = driver.find_elements_by_class_name('clue')
    
    for clue in clues:
       
        clue_text = clue.find_element_by_class_name('clueText').text
        print(f'Clue {clue_text}')
    
    # End the Selenium browser session
    driver.quit



# def get_latest_hints_across_down(crossword_url):
#     response = requests.get(crossword_url)
#     if response.ok:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         # Find the clues for words going across and down
#         across_clues = soup.find_all('div', class_='clueDiv crossing-clue', limit=5)
#         down_clues = soup.find_all('div', class_='clueDiv down-clue', limit=5)
        
#         # Extract the clues
#         across_clues_text = [clue.find('span', class_='clueText').get_text(strip=True) for clue in across_clues]
#         down_clues_text = [clue.find('span', class_='clueText').get_text(strip=True) for clue in down_clues]
        
#         # Save clues into a dictionary
#         clues_dict = {
#             'across': across_clues_text,
#             'down': down_clues_text
#         }
#         return clues_dict
#     else:
#         loguru.logger.error(f"Failed to retrieve crossword clues from {crossword_url}")
#         return {}




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
