"""Metric primitives aligned to the ForestSim paper summary table."""

from __future__ import annotations

import numpy as np


def build_confusion_matrix(
    pred_mask: np.ndarray,
    target_mask: np.ndarray,
    num_classes: int,
    ignore_index: int | None = None,
) -> np.ndarray:
    """Accumulate a confusion matrix from prediction and target masks."""

    pred = np.asarray(pred_mask, dtype=np.int64).reshape(-1)
    target = np.asarray(target_mask, dtype=np.int64).reshape(-1)

    valid = (target >= 0) & (target < num_classes)
    if ignore_index is not None:
        valid &= target != ignore_index

    pred = pred[valid]
    target = target[valid]

    confusion = np.zeros((num_classes, num_classes), dtype=np.int64)
    np.add.at(confusion, (target, pred), 1)
    return confusion


def overall_accuracy(confusion: np.ndarray) -> float:
    """Return pixel accuracy over all non-ignored classes."""

    total = float(confusion.sum())
    if total == 0:
        return float("nan")
    return float(np.trace(confusion) / total)


def per_class_iou(confusion: np.ndarray) -> np.ndarray:
    """Return per-class intersection-over-union values."""

    true_positive = np.diag(confusion).astype(np.float64)
    false_positive = confusion.sum(axis=0).astype(np.float64) - true_positive
    false_negative = confusion.sum(axis=1).astype(np.float64) - true_positive
    denom = true_positive + false_positive + false_negative
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(denom > 0, true_positive / denom, np.nan)


def per_class_accuracy(confusion: np.ndarray) -> np.ndarray:
    """Return per-class accuracies."""

    true_positive = np.diag(confusion).astype(np.float64)
    support = confusion.sum(axis=1).astype(np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(support > 0, true_positive / support, np.nan)


def summarize_metrics(confusion: np.ndarray) -> dict[str, float]:
    """Compute the paper-style aggregate metrics from a confusion matrix."""

    iou = per_class_iou(confusion)
    acc = per_class_accuracy(confusion)
    return {
        "aAcc": overall_accuracy(confusion),
        "mIoU": float(np.nanmean(iou)),
        "mAcc": float(np.nanmean(acc)),
    }
