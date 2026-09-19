"""Calculate label distributions, co-occurrence, pairwise, and trio agreement."""

import argparse
from itertools import combinations
from pathlib import Path

import pandas as pd

from calculate_annotation_metrics import binary_scores, majority_vote, model_columns
from locate_release_data import default_release_directory, release_data_paths


CATEGORIES = ("Conspiracy", "Sensationalism", "Hate_Speech", "Speculation", "Satire")
HUMAN_COLUMNS = {category: f"{category.lower()}_majority" for category in CATEGORIES}


def main() -> None:
    release_dir = default_release_directory()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-dir", type=Path, default=release_dir)
    parser.add_argument("--output-dir", type=Path, default=release_dir / "Generated_Output" / "Tables")
    args = parser.parse_args()
    paths = release_data_paths(args.release_dir)
    main_data = pd.read_csv(paths["main"], dtype={"id": "string"}, low_memory=False)
    llm = pd.read_csv(paths["llm"], dtype={"id": "string"}, low_memory=False)
    human = pd.read_csv(paths["human"], dtype={"id": "string"}, low_memory=False)
    merged = human.merge(llm, on="id", how="inner", validate="one_to_one")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    indicators = main_data.loc[:, CATEGORIES].apply(pd.to_numeric, errors="coerce").eq(1)
    label_sets = indicators.apply(lambda row: " | ".join(category for category, selected in row.items() if selected) or "no_labels", axis=1)
    label_sets.value_counts().rename_axis("label_set").reset_index(name="posts").to_csv(args.output_dir / "label_cooccurrence.csv", index=False)
    distribution, pairwise, trios = [], [], []
    for category in CATEGORIES:
        columns = model_columns(llm, category)
        for column in columns:
            distribution.append({"annotator": column.removeprefix(f"{category}_"), "category": category, "positive_count": int(pd.to_numeric(llm[column], errors="coerce").eq(1).sum()), "rows": len(llm)})
        for first, second in combinations(columns, 2):
            pairwise.append({"category": category, "annotator_1": first.removeprefix(f"{category}_"), "annotator_2": second.removeprefix(f"{category}_"), **binary_scores(llm[first], llm[second])})
        for trio in combinations(columns, 3):
            trios.append({"category": category, "models": " | ".join(column.removeprefix(f"{category}_") for column in trio), **binary_scores(merged[HUMAN_COLUMNS[category]], majority_vote(merged, list(trio)))})
        distribution.append({"annotator": "human_majority", "category": category, "positive_count": int(pd.to_numeric(human[HUMAN_COLUMNS[category]], errors="coerce").eq(1).sum()), "rows": len(human)})
    pd.DataFrame(distribution).to_csv(args.output_dir / "label_distribution.csv", index=False)
    pd.DataFrame(pairwise).to_csv(args.output_dir / "llm_pairwise_agreement.csv", index=False)
    pd.DataFrame(trios).to_csv(args.output_dir / "llm_trio_vs_human.csv", index=False)


if __name__ == "__main__":
    main()
