"""Create dataset-size, label-count, and schema tables from released CSVs."""

import argparse
from pathlib import Path

import pandas as pd

from locate_release_data import default_release_directory, release_data_paths


CATEGORIES = ("Conspiracy", "Sensationalism", "Hate_Speech", "Speculation", "Satire")


def main() -> None:
    release_dir = default_release_directory()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-dir", type=Path, default=release_dir)
    parser.add_argument("--output-dir", type=Path, default=release_dir / "Generated_Output" / "Tables")
    args = parser.parse_args()
    paths = release_data_paths(args.release_dir)
    main_data = pd.read_csv(paths["main"], dtype={"id": "string"}, low_memory=False)
    dehydrated = pd.read_csv(paths["dehydrated"], dtype={"id": "string"}, low_memory=False)
    llm = pd.read_csv(paths["llm"], dtype={"id": "string"}, low_memory=False)
    human = pd.read_csv(paths["human"], dtype={"id": "string"}, low_memory=False)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([{"release_file": name, "rows": len(frame), "columns": len(frame.columns)} for name, frame in (("full", main_data), ("dehydrated", dehydrated), ("llm_annotations", llm), ("human_annotations", human))]).to_csv(args.output_dir / "release_input_summary.csv", index=False)
    pd.DataFrame([{"posts": len(main_data), "variables": len(main_data.columns), **{f"{category}_positive": int(pd.to_numeric(main_data[category], errors="coerce").eq(1).sum()) for category in CATEGORIES}}]).to_csv(args.output_dir / "dataset_characteristics.csv", index=False)
    pd.DataFrame({"variable": main_data.columns, "dtype": main_data.dtypes.astype(str), "non_null": main_data.notna().sum(), "non_null_percent": (main_data.notna().mean() * 100).round(4)}).to_csv(args.output_dir / "variable_schema.csv", index=False)


if __name__ == "__main__":
    main()
