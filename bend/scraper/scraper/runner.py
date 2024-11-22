# Example Usage
from scraper.crawler import scrape_sites

if __name__ == "__main__":
    starting_urls = [
        "https://tax.illinois.gov",
    ]

    scrape_sites(starting_urls, "../output")
