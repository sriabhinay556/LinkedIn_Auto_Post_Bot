from ai_scraper import ai_scraper
from parse_article_page import parse_article_page
async def crawl_articles(articles_data):
    # Check if articles_data is a list of dictionaries
    if not isinstance(articles_data, list) or not all(isinstance(article, dict) for article in articles_data):
        raise TypeError("Expected articles_data to be a list of dictionaries")

    all_articles_content = []
    
    for article in articles_data[:4]:
        crawl_url = article["link"]
        response_from_ai_scraper = await ai_scraper(crawl_url)
        article_content = parse_article_page(response_from_ai_scraper)
        all_articles_content.append({
            "article_content": article_content,
            "article": article
        })
    print(all_articles_content)
    return all_articles_content
