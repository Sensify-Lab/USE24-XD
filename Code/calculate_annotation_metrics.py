"""Shared binary-label metrics for agreement and validation calculations."""

from itertools import combinations

import numpy as np
import pandas as pd


def model_columns(frame: pd.DataFrame, category: str) -> list[str]:
    return sorted(column for column in frame.columns if column.startswith(f"{category}_"))


def majority_vote(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    values = frame.loc[:, columns].apply(pd.to_numeric, errors="coerce")
    return values.mean(axis=1).ge(0.5).where(values.notna().any(axis=1))


def cohen_kappa(truth: pd.Series, prediction: pd.Series) -> float:
    paired = pd.DataFrame({"truth": truth, "prediction": prediction}).dropna().astype(int)
    if paired.empty:
        return float("nan")
    observed = (paired["truth"] == paired["prediction"]).mean()
    expected = sum((paired["truth"] == value).mean() * (paired["prediction"] == value).mean() for value in (0, 1))
    return float("nan") if expected == 1 else float((observed - expected) / (1 - expected))


def binary_scores(truth: pd.Series, prediction: pd.Series) -> dict[str, float | int]:
    paired = pd.DataFrame({"truth": truth, "prediction": prediction}).dropna().astype(int)
    if paired.empty:
        return {"n_evaluated": 0, "accuracy": float("nan"), "precision": float("nan"), "recall": float("nan"), "f1": float("nan"), "cohen_kappa": float("nan")}
    true_positive = ((paired["truth"] == 1) & (paired["prediction"] == 1)).sum()
    false_positive = ((paired["truth"] == 0) & (paired["prediction"] == 1)).sum()
    false_negative = ((paired["truth"] == 1) & (paired["prediction"] == 0)).sum()
    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    return {"n_evaluated": len(paired), "accuracy": float((paired["truth"] == paired["prediction"]).mean()), "precision": precision, "recall": recall, "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0, "cohen_kappa": cohen_kappa(paired["truth"], paired["prediction"])}


def all_model_trios(columns: list[str]):
    return combinations(columns, 3)


def stratified_folds(labels: pd.Series, seed: int, folds: int = 5) -> list[tuple[np.ndarray, np.ndarray]]:
    random = np.random.default_rng(seed)
    pieces = [[] for _ in range(folds)]
    for value in sorted(labels.dropna().unique()):
        indices = np.flatnonzero(labels.to_numpy() == value)
        random.shuffle(indices)
        for fold, part in enumerate(np.array_split(indices, folds)):
            pieces[fold].extend(part.tolist())
    all_indices = np.arange(len(labels))
    return [(all_indices[~np.isin(all_indices, test)], np.array(sorted(test), dtype=int)) for test in pieces]
