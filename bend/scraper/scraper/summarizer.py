import os
from typing import List

from api.utils.fs import read_json, write_json
from api.utils.llm import complete_batch
from scraper.models import RecordSummary
from scraper.prompts import ITEM_EXTRACTION_PROMPT
from scraper.web import get_webpages


def summarize(output_path: str):
    input_path = os.path.join(output_path, "records.json")

    # Extract records
    records = read_json(input_path)[0]
    source2record = {r["source"]: r for r in records}
    source_links = list(source2record.keys())

    # Download webpages
    source2content = get_webpages(source_links)

    # Summarizes records
    source_links = list(source2content.keys())
    prompts = [ITEM_EXTRACTION_PROMPT.format(source2content[s]) for s in source_links]
    summaries: List[RecordSummary] = complete_batch(prompts, RecordSummary)
    for url, summary_item in zip(source_links, summaries):
        if summary_item is None:
            continue
        summary = summary_item.summary
        if summary.strip().startswith("NA"):
            print("URL did not contain tax info:", url)
            continue
        if url not in source2record:
            print("Something weird happened with:", url)
            continue

        source2record[url]["description"] = summary

    # Write output
    final_records = list(source2record.values())
    write_json(final_records, os.path.join(output_path, "final.json"))


if __name__ == '__main__':
    summarize('../output')
