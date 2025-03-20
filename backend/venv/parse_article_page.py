from bs4 import BeautifulSoup

def parse_article_page(artcile_html):

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(artcile_html, "html.parser")

    # Find the main content area
    main_content = soup.find("main", class_="wp-block-group template-content is-layout-constrained wp-block-group-is-layout-constrained")

    # Extract the text from each paragraph within the main content area
    article_text = ""
    if main_content:
        paragraphs = main_content.find_all("p", class_="wp-block-paragraph")
        for paragraph in paragraphs:
            article_text += paragraph.get_text() + "\n"

    # Display the article content
    return article_text
