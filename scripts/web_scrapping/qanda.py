import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def get_faqs_from_url(url):
    """
    Scrapes a given URL to find and print FAQ content.
    """
    try:
        # Set a User-Agent header to mimic a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the URL content
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Keywords and common selectors to look for
        faq_keywords = ['faq', 'frequently asked questions', 'q&a', 'help center']
        faq_selectors = ['div', 'section', 'ul', 'article']
        
        found_faqs = False
        
        # Search for elements containing the keywords
        for selector in faq_selectors:
            for element in soup.find_all(selector):
                # Check if the text or ID/class contains an FAQ keyword
                if any(keyword in element.get_text().lower() for keyword in faq_keywords) or \
                   any(keyword in str(element.get('id', '')).lower() for keyword in faq_keywords) or \
                   any(keyword in str(element.get('class', '')).lower() for keyword in faq_keywords):
                    
                    # Print the found content and a separator
                    print(f"--- Found FAQ content from {url} ---")
                    print(element.get_text(separator="\n", strip=True))
                    print("-" * 50)
                    found_faqs = True
                    break
            if found_faqs:
                break
        
        if not found_faqs:
            print(f"--- No clear FAQ section found on {url} ---")
        
    except RequestException as e:
        print(f"--- Error accessing {url}: {e} ---")

# Define the array of URLs you want to scrape
urls_to_scrape = [
    'https://www.apple.com/shop/help/payments',
    'https://www.amazon.com/gp/help/customer/display.html?nodeId=GN7B6F3E689C8G6Z'
]

# Iterate through the URL array and call the scraper function
for url in urls_to_scrape:
    get_faqs_from_url(url)