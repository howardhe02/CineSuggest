"""
This program calls upon GoogleImageScraper.py and scrapes images off google. The scraped
images are used to display images in the program.
"""
from GoogleImageScrapper import GoogleImageScraper
import os
from typing import Tuple

# File Path
webdriver_path = os.path.normpath(os.getcwd() + "\\Google-Image-Scraper-master\\webdriver\\chromedriver.exe")

def run_scrapy(search_keys: list, number_of_images: int, min_resolution: Tuple[int, int],
               max_resolution: Tuple[int, int], image_path: str) -> None:
    """Calls upon GoogleImageScraper to scrape and download images off the web.

    Args:
        search_keys: List of search terms for the images to be scraped.
        number_of_images: Number of images to attempt to download for each search term.
        min_resolution: Minimum resolution of images to be downloaded.
        max_resolution: Maximum resolution of images to be downloaded.
        image_path: Path to the folder where images will be saved.
    """
    for search_key in search_keys:
        image_scrapper = GoogleImageScraper(webdriver_path, image_path, search_key,
                                            number_of_images, headless=False,
                                            min_resolution=min_resolution, max_resolution=max_resolution)
        image_urls = image_scrapper.find_image_urls()
        image_scrapper.save_images(image_urls)
