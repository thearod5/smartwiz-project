import json
import time
from typing import List

import requests
import requests_cache
from bs4 import BeautifulSoup

from scraper.constants import RATE_LIMIT_SLEEP
from scraper.llm import analyze_content_with_anthropic
from scraper.models import CreditDeduction, URLBatch

requests_cache.install_cache("scraper_cache", backend="sqlite")


def scrape_sites(starting_urls: List[str], output_path: str, max_iterations: int = 10):
    batch = [URLBatch(url=url) for url in starting_urls]
    collected_credits = []
    seen_urls = set()

    for iteration in range(max_iterations):
        print(f"Starting iteration {iteration + 1}...")
        new_links = []

        for item in batch:
            if item.explored or item.url in seen_urls:
                continue
            try:
                # Cached GET request
                response = requests.get(item.url, timeout=10)
                time.sleep(RATE_LIMIT_SLEEP)  # Adjust sleep for rate limiting

                if response.status_code == 200:
                    html_content = response.text
                    seen_urls.add(item.url)

                    # Extract credits/deductions
                    credits = analyze_content_with_anthropic(html_content, item.url)
                    collected_credits.extend(credits)

                    # Save progress to JSON file
                    save_results_to_json(collected_credits, output_path)

                    # Extract new links for further exploration
                    page_links = extract_links(html_content, item.url)
                    new_links.extend(page_links)

                    # Mark as explored
                    item.explored = True
                else:
                    print(f"Failed to fetch {item.url}: HTTP {response.status_code}")
            except Exception as e:
                print(f"Error fetching {item.url}: {e}")

        # Add new links to the batch
        unique_new_links = [URLBatch(url=link) for link in set(new_links) if link not in seen_urls]
        batch.extend(unique_new_links)

        # Stop if no new links are added
        if not unique_new_links:
            print("No new links found, stopping.")
            break

    print(f"Scraping completed. Found {len(collected_credits)} credits/deductions.")
    save_results_to_json(collected_credits, output_path)  # Final save
    return collected_credits


# Function to Extract Links
def extract_links(html_content: str, base_url: str) -> List[str]:
    soup = BeautifulSoup(html_content, "html.parser")
    links = [a['href'] for a in soup.find_all('a', href=True)]
    # Resolve relative URLs
    resolved_links = [requests.compat.urljoin(base_url, link) for link in links]
    return resolved_links


# Function to save results to a JSON file
def save_results_to_json(data: List[CreditDeduction], output_path: str):
    try:
        with open(output_path, "w") as f:
            json.dump([item.dict() for item in data], f, indent=2)
        print(f"Results successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving results to {output_path}: {e}")
