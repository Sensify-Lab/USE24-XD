"""Select LLM trios and score deterministic five-fold held-out validation."""

import argparse
from itertools import combinations
from pathlib import Path

import pandas as pd

from calculate_annotation_metrics import binary_scores, majority_vote, model_columns, stratified_folds
from locate_release_data import default_release_directory, release_data_paths


CATEGORIES = ("Conspiracy", "Sensationalism", "Hate_Speech", "Speculation", "Satire")
HUMAN_COLUMNS = {category: f"{category.lower()}_majority" for category in CATEGORIES}


def main() -> None:
    release_dir = default_release_directory()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-dir", type=Path, default=release_dir)
    parser.add_argument("--output-dir", type=Path, default=release_dir / "Generated_Output" / "Tables")
    parser.add_argument("--seed", type=int, default=20260816)
    args = parser.parse_args()
    paths = release_data_paths(args.release_dir)
    llm = pd.read_csv(paths["llm"], dtype={"id": "string"}, low_memory=False)
    human = pd.read_csv(paths["human"], dtype={"id": "string"}, low_memory=False)
    merged = human.merge(llm, on="id", how="inner", validate="one_to_one")
    rows = []
    for category in CATEGORIES:
        data = merged.dropna(subset=[HUMAN_COLUMNS[category]]).reset_index(drop=True)
        columns = model_columns(data, category)
        for fold, (train_index, test_index) in enumerate(stratified_folds(data[HUMAN_COLUMNS[category]], args.seed), start=1):
            train, test = data.iloc[train_index], data.iloc[test_index]
            candidates = [(binary_scores(train[HUMAN_COLUMNS[category]], majority_vote(train, list(trio))), trio) for trio in combinations(columns, 3)]
            training, selected = sorted(candidates, key=lambda item: (-item[0]["cohen_kappa"], item[1]))[0]
            heldout = binary_scores(test[HUMAN_COLUMNS[category]], majority_vote(test, list(selected)))
            rows.append({"category": category, "fold": fold, "models": " | ".join(column.removeprefix(f"{category}_") for column in selected), **{f"training_{key}": value for key, value in training.items()}, **{f"heldout_{key}": value for key, value in heldout.items()}})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(args.output_dir / "fivefold_trio_validation.csv", index=False)


if __name__ == "__main__":
    main()
