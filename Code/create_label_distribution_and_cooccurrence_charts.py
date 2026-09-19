"""Create label-distribution and label-cooccurrence charts from generated tables."""

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

    distribution = pd.read_csv(args.table_dir / "label_distribution.csv")
    distribution["percentage"] = 100 * distribution["positive_count"] / distribution["rows"]
    chart = distribution.pivot(index="category", columns="annotator", values="percentage").reindex(CATEGORIES)
    chart.index = [category.replace("_", " ") for category in chart.index]
    axis = chart.plot.bar(figsize=(8, 4.5), ylabel="Posts labelled positive (%)")
    axis.set_xlabel("Label"); axis.legend(title="Annotator", frameon=False)
    plt.tight_layout(); plt.savefig(args.output_dir / "label_distribution.pdf"); plt.close()
    cooccurrence = pd.read_csv(args.table_dir / "label_cooccurrence.csv").nlargest(15, "posts").sort_values("posts")
    plt.figure(figsize=(9, 5)); plt.barh(cooccurrence["label_set"], cooccurrence["posts"], color="#3C78A8")
    plt.xlabel("Posts"); plt.ylabel("Concurrent label set"); plt.tight_layout(); plt.savefig(args.output_dir / "label_cooccurrence.pdf"); plt.close()


if __name__ == "__main__":
    main()
