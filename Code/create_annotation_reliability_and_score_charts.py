"""Create reliability and LLM-trio score charts from generated tables."""

import argparse
import os
from pathlib import Path

import pandas as pd

from locate_release_data import default_release_directory


CATEGORIES = ("Conspiracy", "Sensationalism", "Hate_Speech", "Speculation", "Satire")


def main() -> None:
    release_dir = default_release_directory()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table-dir", type=Path, default=release_dir / "Generated_Output" / "Tables")
    parser.add_argument("--output-dir", type=Path, default=release_dir / "Generated_Output" / "Visualizations")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(args.output_dir / ".matplotlib"))
    import matplotlib.pyplot as plt

    labels = [category.replace("_", " ") for category in CATEGORIES]
    llm = pd.read_csv(args.table_dir / "llm_trio_krippendorff_alpha.csv")
    human = pd.read_csv(args.table_dir / "human_krippendorff_alpha.csv").set_index("category").reindex(CATEGORIES)
    plt.figure(figsize=(8, 4.5)); plt.boxplot([llm.loc[llm["category"] == category, "krippendorff_alpha"].dropna() for category in CATEGORIES], tick_labels=labels, showmeans=True)
    plt.ylabel("Krippendorff's alpha"); plt.ylim(-1, 1); plt.xticks(rotation=25, ha="right"); plt.tight_layout(); plt.savefig(args.output_dir / "llm_reliability.pdf"); plt.close()
    plt.figure(figsize=(8, 4.5)); plt.bar(labels, human["krippendorff_alpha"], color="#CE7D3A")
    plt.axhline(0, color="black", linewidth=0.8); plt.ylabel("Krippendorff's alpha"); plt.ylim(-1, 1); plt.xticks(rotation=25, ha="right"); plt.tight_layout(); plt.savefig(args.output_dir / "human_reliability.pdf"); plt.close()
    scores = pd.read_csv(args.table_dir / "llm_trio_vs_human.csv")
    chart, axes = plt.subplots(1, 3, figsize=(11, 4.5), sharey=True)
    for axis, metric in zip(axes, ("precision", "recall", "f1"), strict=True):
        axis.violinplot([scores.loc[scores["category"] == category, metric].dropna() for category in CATEGORIES], showmeans=True, showextrema=False)
        axis.set_title(metric.capitalize()); axis.set_xticks(range(1, 6), labels, rotation=25, ha="right"); axis.set_ylim(0, 1)
    axes[0].set_ylabel("Score against human majority"); chart.tight_layout(); chart.savefig(args.output_dir / "llm_trio_scores.pdf"); plt.close(chart)


if __name__ == "__main__":
    main()
