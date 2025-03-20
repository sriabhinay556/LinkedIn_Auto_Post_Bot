import json

def parse_main_page(html_content):
    from bs4 import BeautifulSoup
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all article sections within 'loop-card__content' divs
    articles = soup.find_all("div", class_="loop-card__content")

    # Initialize a list to store article data
    articles_data = []

    # Loop through each article section and extract details
    for article in articles:
        # Category
        category_tag = article.find("a", class_="loop-card__cat")
        category = category_tag.get_text(strip=True) if category_tag else "No category"
        
        # Title and link
        title_tag = article.find("h3", class_="loop-card__title").find("a", class_="loop-card__title-link")
        title = title_tag.get_text(strip=True) if title_tag else "No title"
        link = title_tag['href'] if title_tag else "No link"
        
        # Author
        author_tag = article.find("a", class_="loop-card__author")
        author = author_tag.get_text(strip=True) if author_tag else "No author"
        
        # Date
        date_tag = article.find("time")
        date = date_tag['datetime'] if date_tag else "No date"
        
        # Append the data to the list as a dictionary
        articles_data.append({
            "category": category,
            "title": title,
            "link": link,
            "author": author,
            "date": date
        })

    # Return the data as a JSON array
    

    return articles_data