import os
import time
from typing import Dict, List, Set

import requests
import requests_cache
from PyPDF2 import PdfReader
from tqdm import tqdm

from scraper.constants import RATE_LIMIT_SLEEP

requests_cache.install_cache("scraper_cache", backend="sqlite")


def get_webpages(webpages: List[str], seen_urls: Set[str] = None) -> Dict[str, str]:
    """
    Requests content for list of webpages and processes PDFs if encountered.
    :param webpages: List of URLs to webpages or PDFs.
    :param seen_urls: List of already processed urls, used to skip crawling.
    :return: Dictionary mapping url to content (HTML or extracted PDF text).
    """
    seen_urls = seen_urls or set()
    url2content = {}

    for url in tqdm(webpages, desc="Download webpages/PDFs"):
        if url in seen_urls:
            continue
        try:
            # Check if the URL points to a PDF file
            if url.endswith(".pdf"):
                pdf_path = f"temp_{os.path.basename(url)}"
                save_pdf(url, pdf_path)
                text_content = extract_text_from_pdf(pdf_path)
                url2content[url] = text_content
                os.remove(pdf_path)  # Clean up the temporary file
            else:
                # Cached GET request for normal webpages
                response = requests.get(url, timeout=10)
                time.sleep(RATE_LIMIT_SLEEP)  # Adjust sleep for rate limiting

                if response.status_code == 200:
                    html_content = response.text
                    url2content[url] = html_content
                else:
                    print(f"Failed to fetch {url}: HTTP {response.status_code}")

            seen_urls.add(url)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    return url2content


def save_pdf(url: str, save_path: str) -> str:
    """
    Downloads a PDF file from a URL and saves it locally.
    :param url: URL of the PDF.
    :param save_path: Path to save the downloaded PDF.
    :return: Path to the saved PDF.
    """
    response = requests.get(url, stream=True, timeout=10)
    if response.status_code == 200:
        with open(save_path, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=1024):
                pdf_file.write(chunk)
        return save_path
    else:
        raise Exception(f"Failed to fetch {url}: HTTP {response.status_code}")


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.
    :param pdf_path: Path to the PDF file.
    :return: Extracted text from the PDF.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""
