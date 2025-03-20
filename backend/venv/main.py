from ai_scraper import ai_scraper
import asyncio
import os
from dotenv import load_dotenv
import json
from parse_main_page import parse_main_page
from crawl_articles import crawl_articles
from flask import Flask, jsonify

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

async def main():
    url = "https://techcrunch.com/latest/"
    response_from_ai_scraper = await ai_scraper(url)
    list_of_articles = parse_main_page(response_from_ai_scraper)
    all_articles_data = await crawl_articles(list_of_articles)
    return all_articles_data

@app.route('/scrape', methods=['GET'])
def scrape():
    # Run the async main function and return the result
    all_articles_data = asyncio.run(main())
    return jsonify(all_articles_data)
    

if __name__ == "__main__":
    app.run(debug=True)
