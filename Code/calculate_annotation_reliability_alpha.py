"""Calculate Krippendorff alpha for released LLM and human annotations."""

import argparse
from itertools import combinations
from pathlib import Path

import pandas as pd

from calculate_annotation_metrics import model_columns
from locate_release_data import default_release_directory, release_data_paths


CATEGORIES = ("Conspiracy", "Sensationalism", "Hate_Speech", "Speculation", "Satire")


def alpha(frame: pd.DataFrame, columns: list[str]) -> float:
    import krippendorff

    return float(krippendorff.alpha(reliability_data=frame.loc[:, columns].apply(pd.to_numeric, errors="coerce").to_numpy().T, level_of_measurement="nominal"))


def main() -> None:
    release_dir = default_release_directory()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-dir", type=Path, default=release_dir)
    parser.add_argument("--output-dir", type=Path, default=release_dir / "Generated_Output" / "Tables")
    args = parser.parse_args()
    paths = release_data_paths(args.release_dir)
    llm = pd.read_csv(paths["llm"], dtype={"id": "string"}, low_memory=False)
    human = pd.read_csv(paths["human"], dtype={"id": "string"}, low_memory=False)
    llm_rows, human_rows = [], []
    for category in CATEGORIES:
        for trio in combinations(model_columns(llm, category), 3):
            llm_rows.append({"category": category, "models": " | ".join(column.removeprefix(f"{category}_") for column in trio), "krippendorff_alpha": alpha(llm, list(trio))})
        columns = [f"{category.lower()}{number}" for number in range(1, 4)]
        human_rows.append({"category": category, "raters": "three human annotations", "krippendorff_alpha": alpha(human, columns)})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(llm_rows).to_csv(args.output_dir / "llm_trio_krippendorff_alpha.csv", index=False)
    pd.DataFrame(human_rows).to_csv(args.output_dir / "human_krippendorff_alpha.csv", index=False)


if __name__ == "__main__":
    main()
