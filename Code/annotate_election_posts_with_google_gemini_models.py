"""Annotate a released or collected post CSV with a Google Gemini model."""

import argparse
import os
from pathlib import Path

import pandas as pd

from define_election_post_annotation_labels import annotation_prompt, annotation_row
from locate_release_data import default_release_directory, release_data_paths


def main() -> None:
    release_dir = default_release_directory()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", type=Path, default=release_data_paths(release_dir)["main"])
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--model", default="gemini-2.0-flash")
    parser.add_argument("--output-csv", type=Path, default=release_dir / "Generated_Output" / "Annotations" / "gemini_annotations.csv")
    args = parser.parse_args()
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Set GEMINI_API_KEY before running annotation.")
    from google import genai

    source = pd.read_csv(args.input_csv, dtype={"id": "string"}, low_memory=False)
    if args.text_column not in source:
        raise ValueError(f"Missing text column: {args.text_column}")
    client, rows = genai.Client(api_key=key), []
    for row in source.loc[:, ["id", args.text_column]].itertuples(index=False):
        response = client.models.generate_content(model=args.model, contents=annotation_prompt(str(row[1])), config={"response_mime_type": "application/json", "temperature": 0})
        rows.append(annotation_row(row[0], response.text or "{}"))
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main()
