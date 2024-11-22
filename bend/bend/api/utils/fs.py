import json
from typing import Any, List


def write_json(data: List[Any], output_path: str):
    try:
        with open(output_path, "w") as f:
            json.dump([data], f, indent=2)
    except Exception as e:
        print(f"Error saving results to {output_path}: {e}")


def read_json(f_path: str) -> str:
    with open(f_path) as f:
        return json.load(f)
