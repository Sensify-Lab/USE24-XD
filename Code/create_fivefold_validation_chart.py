"""Create the five-fold validation chart from the generated validation table."""

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
    validation = pd.read_csv(args.table_dir / "fivefold_trio_validation.csv")
    chart, axes = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
    for axis, metric, title in zip(axes, ("cohen_kappa", "recall"), ("Cohen's kappa", "Recall"), strict=True):
        for source, marker in (("training", "o"), ("heldout", "s")):
            axis.plot(labels, validation.groupby("category")[f"{source}_{metric}"].mean().reindex(CATEGORIES), marker=marker, label=source.capitalize())
        axis.set_ylim(-1 if metric == "cohen_kappa" else 0, 1); axis.set_ylabel(title); axis.legend(frameon=False, ncol=2)
    plt.xticks(rotation=25, ha="right"); chart.tight_layout(); chart.savefig(args.output_dir / "fivefold_validation.png", dpi=300); plt.close(chart)


if __name__ == "__main__":
    main()
