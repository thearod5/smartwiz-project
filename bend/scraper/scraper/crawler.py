import os
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from scraper.llm import complete_batch
from scraper.models import Record
from scraper.prompts import ITEM_EXTRACTION_PROMPT, LINK_EXTRACTION_PROMPT
from scraper.util import write_json
from scraper.web import get_webpages

FILE_EXTENSIONS = [".pdf"]


def scrape_sites(starting_urls: List[str], output_path: str, max_iterations: int = 10):
    global_records: List[Dict] = []
    global_links = []
    global_files = []
    seen_urls = set()

    batch = starting_urls

    for iteration in range(max_iterations):
        # Save batches
        global_links.append(batch)
        write_json(global_links, os.path.join(output_path, "links.json"))

        # Process current batch
        print(f"Starting batch ({len(batch)}...")
        url2content = get_webpages(batch, seen_urls)
        records = extract_items(url2content)
        global_records.extend(records)
        for record in records:
            seen_urls.add(record["source"])
        for link in batch:
            seen_urls.add(link)
        write_json(global_records, os.path.join(output_path, "records.json"))

        # Extract new links for further exploration
        batch = get_next_batch(url2content)
        files = [f for f in batch if any([f.endswith(ext) for ext in FILE_EXTENSIONS])]
        batch = [f for f in batch if f not in files]

        batch = list(set(batch).difference(seen_urls))
        global_files.extend(files)
        write_json(global_files, os.path.join(output_path, "files.json"))
        if len(batch) == 0:
            print("No new links found, stopping.")
            break
    return global_records


class ExtractionResponse(BaseModel):
    """
    The extracted credits or deductions from webpage.
    """
    records: List[Record] = Field(..., description="List of credits or deductions extracted from content.")


def extract_items(url2content: Dict[str, str]) -> List[Record]:
    urls = list(url2content.keys())  # serialize order
    contents = [url2content[url] for url in urls]
    prompts = [ITEM_EXTRACTION_PROMPT.format(c) for c in contents]
    extractions: List[ExtractionResponse] = complete_batch(prompts, ExtractionResponse)

    items = []
    for url, extraction in zip(urls, extractions):
        if extraction is None:
            print(f"URL content was not parseable: {url}")
            continue
        items.extend([r.dict() for r in extraction.records])

    return items


class LinkExtractor(BaseModel):
    """
    Lists links to webpages that might contain credits or deduction for the state.
    """
    links: List[str] = Field(..., description="List of links that may define credits or deductions.")


def get_next_batch(url2content: Dict[str, str], batch_size=15, max_links_per_batch: int = 5) -> List[str]:
    """
    Prompts model to select links that might contains records.
    :param url2content: The current content of batch.
    :return: new links to explore
    """
    links = get_html_links(url2content)

    # create batches
    link_batches = [links[i: i + batch_size] for i in range(0, len(links), batch_size)]
    prompts = []
    for link_batch in link_batches:
        link_batch_display = "\n".join([f"{i + 1}) {l}" for i, l in enumerate(link_batch)])
        prompt = LINK_EXTRACTION_PROMPT.format(link_batch_display)
        prompts.append(prompt)

    responses: List[LinkExtractor] = complete_batch(prompts, LinkExtractor)
    new_links = []
    for response in responses:
        if response is None:
            continue
        new_links.extend(response.links[:max_links_per_batch])

    new_links = [url.rstrip('/') for url in new_links]
    return new_links


def get_html_links(url2content: Dict[str, str]) -> List[str]:
    global_links = []
    for url, content in url2content.items():
        soup = BeautifulSoup(content, "html.parser")
        links = [a['href'] for a in soup.find_all('a', href=True)]
        # Resolve relative URLs
        resolved_links = [link if link.startswith("http") else requests.compat.urljoin(url, link) for link in links]
        global_links.extend(resolved_links)
    return global_links
