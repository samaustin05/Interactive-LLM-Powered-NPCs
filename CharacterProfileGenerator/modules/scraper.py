# modules/scraper.py
import requests
from bs4 import BeautifulSoup
import logging
import os

class Scraper:
    def scrape_fandom_page(self, url):
        logging.debug(f"Starting to scrape URL: {url}")
        try:
            response = requests.get(url)
            logging.debug(f"Received status code {response.status_code} for URL: {url}")
            if response.status_code != 200:
                raise Exception(f"Failed to fetch page: {url}, Status Code: {response.status_code}")
            soup = BeautifulSoup(response.content, 'html.parser')
            content_div = soup.find('div', {'class': 'mw-parser-output'})
            if not content_div:
                raise Exception(f"Could not find content div in {url}")

            # Remove unwanted elements
            unwanted_tags = ['table', 'div', 'span', 'img', 'sup', 'ul', 'ol', 'h2', 'h3', 'h4']
            for tag in content_div.find_all(unwanted_tags):
                tag.decompose()
            logging.debug(f"Unwanted elements removed from the page: {url}")

            text = content_div.get_text(separator='\n', strip=True)
            logging.info(f"Successfully scraped data from {url}")
            return text
        except Exception as e:
            logging.error(f"Error scraping {url}: {e}")
            raise
