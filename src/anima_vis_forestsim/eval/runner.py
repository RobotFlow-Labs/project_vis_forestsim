"""Evaluation runner for deterministic local benchmark sweeps."""

from __future__ import annotations

from typing import Any

import numpy as np

from .metrics import build_confusion_matrix, summarize_metrics


def _unpack_example(example: Any) -> tuple[np.ndarray, np.ndarray]:
    if isinstance(example, dict):
        return np.asarray(example["image"]), np.asarray(example["target_mask"])
    if isinstance(example, (tuple, list)) and len(example) == 2:
        return np.asarray(example[0]), np.asarray(example[1])
    raise TypeError("Each eval example must be a dict or a 2-tuple of (image, target_mask).")


def run_eval(
    predictor: Any,
    split: list[Any],
    checkpoint_id: str = "m12",
    ontology: str = "forestsim24",
) -> dict[str, float]:
    """Run a local evaluation sweep over synthetic or staged examples."""

    if not split:
        raise ValueError("Evaluation split must contain at least one example.")

    total_confusion: np.ndarray | None = None
    for example in split:
        image, target_mask = _unpack_example(example)
        result = predictor.predict(image, checkpoint_id=checkpoint_id, ontology=ontology)
        pred_mask = result.mask

        if pred_mask.shape != target_mask.shape:
            raise ValueError(
                f"Prediction shape {pred_mask.shape} does not match target shape {target_mask.shape}."
            )

        confusion = build_confusion_matrix(
            pred_mask=pred_mask,
            target_mask=target_mask,
            num_classes=result.logits.shape[1],
        )
        if total_confusion is None:
            total_confusion = confusion
        else:
            total_confusion += confusion

    summary = summarize_metrics(total_confusion)
    summary["num_examples"] = float(len(split))
    return summary
