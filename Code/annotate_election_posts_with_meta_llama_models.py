"""Annotate a released or collected post CSV with a Meta Llama endpoint."""

import argparse
import os
from pathlib import Path

import pandas as pd

from define_election_post_annotation_labels import annotation_messages, annotation_row
from locate_release_data import default_release_directory, release_data_paths


def main() -> None:
    release_dir = default_release_directory()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", type=Path, default=release_data_paths(release_dir)["main"])
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--model", default="meta-llama/Llama-3.3-70B-Instruct")
    parser.add_argument("--base-url", default="https://router.huggingface.co/v1")
    parser.add_argument("--output-csv", type=Path, default=release_dir / "Generated_Output" / "Annotations" / "llama_annotations.csv")
    args = parser.parse_args()
    token = os.environ.get("HF_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Set HF_TOKEN before running annotation.")
    from openai import OpenAI

    source = pd.read_csv(args.input_csv, dtype={"id": "string"}, low_memory=False)
    if args.text_column not in source:
        raise ValueError(f"Missing text column: {args.text_column}")
    client, rows = OpenAI(api_key=token, base_url=args.base_url), []
    for row in source.loc[:, ["id", args.text_column]].itertuples(index=False):
        response = client.chat.completions.create(model=args.model, messages=annotation_messages(str(row[1])), temperature=0, response_format={"type": "json_object"})
        rows.append(annotation_row(row[0], response.choices[0].message.content or "{}"))
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main()
