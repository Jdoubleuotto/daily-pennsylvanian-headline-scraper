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

def get_latest_crossword_url():
    response = requests.get("https://www.thedp.com/section/crosswords")
    
    if response.ok:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        # Find the <a> tag with the link to the crossword
        crossword_link = soup.find('h3', class_= 'standard-link')
        # If the <a> tag is found, return the href attribute (the URL)
        if crossword_link and crossword_link.find('a'):
            url_before = crossword_link.find('a')
            url_after = url_before['href']
            return url_after
        else:
            loguru.logger.info("Crossword link not found.")
            return None
    else:
        print(f"Failed to retrieve page content, status code: {response.status_code}")
        return None


def scrape_data_point():
    """
    Scrapes the author's name and publishing time from an article on The Daily Pennsylvanian.

    Returns:
        dict: A dictionary containing the author's name and publishing time if found, otherwise empty.
    """
    crossword_url = get_latest_crossword_url()
    if crossword_url:
        url = get_latest_crossword_url()
        req = requests.get(url)
        loguru.logger.info(f"Request URL: {req.url}")
        loguru.logger.info(f"Request status code: {req.status_code}")

        if req.ok:
            soup = bs4.BeautifulSoup(req.text, "html.parser")
            author_element = soup.find("a", class_="author-name")
            time_element = soup.find("span", class_="dateline")
            data = {
                "author": author_element.text.strip() if author_element else "No author found",
                "publish_time": time_element.text.strip() if time_element else "No publish time found"
            }
            loguru.logger.info(f"Data: {data}")
            return data
        else:
            loguru.logger.error("Failed to retrieve the page.")
            return {"author": "", "publish_time": ""}
    else:
        loguru.logger.error("Failed to get the latest crossword URL.")
        return {"author": "", "publish_time": ""}





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
