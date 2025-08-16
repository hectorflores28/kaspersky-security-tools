import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import ssl

def get_faqs_from_url(url):
    """
    Scrapes a given URL to find and print FAQ content, handling SSL and 403 errors.
    """
    try:
        # Define headers to mimic a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': url # Referer header can sometimes help with 403 errors
        }
        
        # Fetch the URL content, with SSL verification turned off
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Keywords and common selectors to look for
        faq_keywords = ['faq', 'frequently asked questions', 'q&a', 'help center', 'preguntas frecuentes']
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
        
    except requests.exceptions.HTTPError as errh:
        print(f"--- HTTP Error accessing {url}: {errh} ---")
    except requests.exceptions.ConnectionError as errc:
        print(f"--- Connection Error accessing {url}: {errc} ---")
    except requests.exceptions.Timeout as errt:
        print(f"--- Timeout Error accessing {url}: {errt} ---")
    except RequestException as e:
        print(f"--- An unexpected error occurred while accessing {url}: {e} ---")

# Define the array of URLs you want to scrape
urls_to_scrape = [
    'https://www.apple.com/shop/help/payments',
    'https://www.amazon.com/gp/help/customer/display.html?nodeId=GN7B6F3E689C8G6Z'
]

# Disable the SSL warning for requests.get(verify=False)
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Iterate through the URL array and call the scraper function
for url in urls_to_scrape:
    get_faqs_from_url(url.strip()) # .strip() removes whitespace from the URL