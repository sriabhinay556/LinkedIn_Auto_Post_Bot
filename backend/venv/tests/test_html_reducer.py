from html_reducer import cleanup_html, reduce_html
def main():
    # Fetch the raw HTML from some source
    raw_html = open('raw_html_content.html', 'r', encoding='utf-8').read()
    base_url = "https://www.nike.com/w/little-kids-clothing-6dacez6ymx6z7x4syzv4dh"

    # Step 1: Clean up HTML (remove scripts/styles and extract relevant content)
    title, minimized_body, link_urls, image_urls = cleanup_html(raw_html, base_url)

    # Level 0: Only minify, Level 1: Minify + remove unnecessary attributes, Level 2: Simplify text, remove head, etc.
    reduced_html = reduce_html(minimized_body, reduction=2)

    # Output the final processed HTML into a file
    with open('reduced_html_content.html', 'w', encoding='utf-8') as file:
        file.write(reduced_html)

print("Reduced HTML has been saved to reduced_html_content.html")
if __name__ == "__main__":
    main()  