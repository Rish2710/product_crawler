import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import re
import json
from urllib.parse import urljoin, urlparse
import random


class Crawler:
    def __init__(self, domains):
        """
        Initialize the Crawler with a list of domains.
        """
        self.domains = domains
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.random_user_agent()
        })

    def random_user_agent(self):
        """
        Return a random User-Agent to mimic different browsers.
        """
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        ]
        return random.choice(user_agents)

    def is_product_url(self, url):
        """
        Dynamically checks if a URL is a product URL based on common patterns.
        """
        product_patterns = [
            r"/product/",
            r"/item/",
            r"/dp/",
            r"/gp/",
            r"/catalogue/",
            r"/goods/",
            r"/shop/",
            r"/view/",
            r"/detail/",
            r"/s\?k=",  # Amazon search query
        ]
        return any(re.search(pattern, url) for pattern in product_patterns)

    def get_all_links(self, domain):
        """
        Fetch all links from a given domain with error handling.
        """
        try:
            print(f"Fetching links from: {domain}")
            response = self.session.get(domain, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            links = [
                urljoin(domain, a["href"])
                for a in soup.find_all("a", href=True)
                if urlparse(urljoin(domain, a["href"])).netloc in domain
            ]

            print(f"Found {len(links)} links on {domain}")
            print("Fetched Links:", links)  # Log fetched links for debugging
            return links

        except requests.exceptions.RequestException as e:
            print(f"Error fetching links from {domain}: {e}")
            return []

    def crawl(self):
        """
        Crawl the provided domains and discover product URLs.
        """
        result = {}
        for domain in self.domains:
            all_links = self.get_all_links(domain)
            if not all_links:
                print(f"No links found on {domain}.")
                continue

            # Filter product URLs
            product_urls = {link for link in all_links if self.is_product_url(link)}
            print(f"Product URLs on {domain}: {product_urls}")  # Log product URLs for debugging
            result[domain] = list(product_urls)

        return result


if __name__ == "__main__":
    # List of domains to crawl
    domains = [
        "https://books.toscrape.com",
        "https://www.amazon.com",
        "https://scrapeme.live/shop",
    ]

    # Initialize crawler
    crawler = Crawler(domains)

    # Crawl and get results
    product_urls = crawler.crawl()

    # Define output file path
    output_file_path = "output.json"

    # Write results to output.json
    try:
        print(f"Attempting to write results to {output_file_path}...")
        with open(output_file_path, "w") as output_file:
            json.dump(product_urls, output_file, indent=4)
        print(f"Product URLs successfully saved to {output_file_path}")
    except IOError as e:
        print(f"Failed to write output file: {e}")
