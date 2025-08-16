import requests
from bs4 import BeautifulSoup
import time
import random
from requests.exceptions import RequestException
import ssl

# A list of common User-Agent strings
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
]

# Disable SSL warnings for this script
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Define the output file name
output_file = "all_faqs.txt"

def get_faqs_from_url(url):
    """
    Scrapes a given URL to find FAQ content and saves it to a file.
    """
    try:
        # Select a random User-Agent from the list
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': url 
        }
        
        # Add a random delay before making the request
        time.sleep(random.uniform(2, 5))
        
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        faq_keywords = ['faq', 'frequently asked questions', 'q&a', 'help center', 'preguntas frecuentes']
        faq_selectors = ['div', 'section', 'ul', 'article', 'main']
        
        found_faqs = False
        
        for selector in faq_selectors:
            for element in soup.find_all(selector):
                if any(keyword in element.get_text().lower() for keyword in faq_keywords) or \
                   any(keyword in str(element.get('id', '')).lower() for keyword in faq_keywords) or \
                   any(keyword in str(element.get('class', '')).lower() for keyword in faq_keywords):
                    
                    faq_content = element.get_text(separator="\n", strip=True)

                    # Append the found FAQs to the text file
                    with open(output_file, "a", encoding="utf-8") as f:
                        f.write(f"--- FAQ content from {url} ---\n")
                        f.write(faq_content)
                        f.write("\n" + "-" * 50 + "\n\n")

                    print(f"--- Successfully saved FAQ content from {url} ---")
                    found_faqs = True
                    break
            if found_faqs:
                break
        
        if not found_faqs:
            print(f"--- No clear FAQ section found on {url} ---")
            
    except requests.exceptions.HTTPError as errh:
        print(f"--- HTTP Error accessing {url}: {errh} ---")
    except RequestException as e:
        print(f"--- An unexpected error occurred while accessing {url}: {e} ---")

# Define the array of URLs you want to scrape
urls_to_scrape = [
    'https://www.apple.com/shop/help/payments',
    'https://www.amazon.com/gp/help/customer/display.html?nodeId=GN7B6F3E689C8G6Z'

# Iterate through the URL array and call the scraper function
for url in urls_to_scrape:
    get_faqs_from_url(url.strip())