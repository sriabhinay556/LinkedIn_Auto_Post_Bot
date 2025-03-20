from html_reducer import cleanup_html, reduce_html
from html_parser import generate_parser_logic
from scraper import scrape_website
from requests.exceptions import Timeout, ProxyError, ConnectionError, RequestException
import random
import requests

proxy_file = "proxies_list_input.txt"

async def get_random_proxy(file_path):
    """Retrieve a random proxy from the proxy file."""
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        if proxies:
            return random.choice(proxies)
        else:
            print("Proxy file is empty.")
            return None
    except Exception as e:
        print(f"Failed to read proxy file: {e}")
        return None

async def ai_scraper(url):
    reduced_html = ""
    html_content = None
    max_retries = 5

    # Attempt scraping directly with Playwright (without proxy)
    try:
        print("Attempting direct scraping with Playwright at local...")
        response = await scrape_website(url, use_proxy=False)

        if response.get("status_code") == 200:
            html_content = response.get("html_content")
            print("Direct scraping successful with Playwright.")
            return html_content
        else:
            print(f"Direct scraping failed with status code: {response.get('status_code')}")
    except Exception as e:
        print(f"Initial headless scraping failed: {e}")

    # # If direct scraping fails, try with proxies
    # print("Attempting scraping with proxies...")

    # for attempt in range(max_retries):
    #     # Get a random proxy
    #     proxy_settings = await get_random_proxy(proxy_file)
    #     if not proxy_settings:
    #         print("No proxies available for scraping.")
    #         break

    #     print(f"Using proxy attempt {attempt + 1} of {max_retries} with proxy: {proxy_settings}")

    #     try:
    #         # Perform the request using the proxy
    #         response = await scrape_website(url, use_proxy=True, proxy_file=proxy_file)

    #         if response.get("status_code") == 200:
    #             html_content = response.get("html_content")
    #             print("Scraping successful with proxy.")
    #             break
    #         else:
    #             print("Received unexpected status code:", response.get("status_code"))

    #     except (Timeout, ProxyError, ConnectionError) as e:
    #         print(f"Network-related error occurred on attempt {attempt + 1}: {e}")
    #     except RequestException as e:
    #         print(f"Request failed on attempt {attempt + 1}: {e}")
    #     except Exception as e:
    #         print(f"An unexpected error occurred on attempt {attempt + 1}: {e}")

    #     # If we've exhausted all retries
    #     if attempt == max_retries - 1:
    #         print("Max retries reached. Unable to get a successful response.")
    #         break

    return html_content if html_content else "Failed to scrape content after multiple attempts."
