import asyncio
import requests
import re
import logging
from bs4 import BeautifulSoup as soup
from TelegramBot import TelegramBot

# CATEGORIES - Pick skills you are interested in freelancer.com and copy link.
CATEGORIES = 'https://www.freelancer.com/jobs/django_web-scraping_python_data-mining_' \
             'microsoft-sql-server_tsql/?languages=en'
MAIN_LINK = "https://www.freelancer.com"

last_job_name = ""  # global var

logging.basicConfig(level=logging.INFO)  # Configure logging

def get_item_name(container):
    """Returns the job name, its description and the link of job detail page."""
    try:
        name_block = container.find("div", {"class": "JobSearchCard-primary-heading"})
        if name_block:
            job_name_element = name_block.find("a", {"class": "JobSearchCard-primary-heading-link"})
            if job_name_element:
                job_name = job_name_element.get_text().strip()
                job_link_element = name_block.find("a", {"class": "JobSearchCard-primary-heading-link"}, href=True)
                if job_link_element:
                    job_link = MAIN_LINK + job_link_element["href"] + "details"
                    job_description_element = container.find("p", {"class": "JobSearchCard-primary-description"})
                    if job_description_element:
                        job_description = job_description_element.get_text().strip()
                        return job_name, job_description, job_link
    except Exception as e:
        logging.error(f"An error occurred in get_item_name: {e}")
        return None, None, None

def get_price_and_bid_count(container):
    """Returns the job price and total number of bids."""
    try:
        price_block = container.find("div", {"class": "JobSearchCard-secondary"})
        if price_block:
            item_price_raw = price_block.find("div", {"class": "JobSearchCard-secondary-price"}).get_text().strip()
            item_price = re.findall(r"([$][\d]+)", item_price_raw)[0] + " Dollar"
            if 'Avg Bid' in item_price_raw:
                item_price += ' Avg Bid'
            count_of_bids = price_block.find("div", {"class": "JobSearchCard-secondary-entry"}).get_text().strip()
            return item_price, count_of_bids
    except Exception as e:
        logging.error(f"An error occurred in get_price_and_bid_count: {e}")
        return None, None

def get_containers():
    """Sends a request and returns all of the div containers for jobs as a list """
    try:
        response = requests.get(CATEGORIES)
        if response.status_code != 200:
            raise requests.ConnectionError

        page_soup = soup(response.text, "html.parser")
        containers = page_soup.find_all("div", {"class": "JobSearchCard-item"})
        return containers
    except requests.RequestException as e:
        logging.error(f"Request failed in get_containers: {e}")
        return []

async def check_last():
    """Checks for the last posted job, if it wasn't previously posted
    then sends job detail to Telegram channel via webhook."""
    global last_job_name
    while True:
        containers = get_containers()
        if containers:
            container = containers[0]
            message = ""
            try:
                job_name, job_description, job_link = get_item_name(container)
            except Exception as e:
                logging.error(f"An error occurred while getting item name: {e}")
            # check if there is a new job
            if job_name and job_name != last_job_name:
                try:
                    job_price, bids_count = get_price_and_bid_count(container)
                except Exception as e:
                    logging.error(f"An error occurred while getting price and bid count: {e}")
                last_job_name = job_name
                message += f"__[{job_name}]({job_link})__"
                message += f"\nBids: **{bids_count}**"
                message += '\n' + 3 * '-' + f"**{job_price}**" + 3 * '-'
                message += f'\n{job_description}'
                await TelegramBot.send_message(message)
        await asyncio.sleep(30)

async def run():
    """Scrapes the first page and then sends all job details to Telegram channel via webhook."""
    containers = get_containers()
    for container in containers:
        message = ""
        try:
            job_name, job_description, job_link = get_item_name(container)
            job_price, bids_count = get_price_and_bid_count(container)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        if job_name:
            message += f"__[{job_name}]({job_link})__"
            message += f"\nBids: **{bids_count}**"
            message += '\n' + 3 * '-' + f"**{job_price}**" + 3 * '-'
            message += f'\n{job_description}'
            try:
                await TelegramBot.send_message(message)
            except Exception as e:
                logging.error(f"An error occurred while sending message: {e}")
        await asyncio.sleep(4)

# Run driver function
if __name__ == "__main__":
    asyncio.run(run())
