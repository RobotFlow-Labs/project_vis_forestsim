"""Evaluation utilities for ForestSim benchmark reproduction."""

from .metrics import (
    build_confusion_matrix,
    overall_accuracy,
    per_class_accuracy,
    per_class_iou,
    summarize_metrics,
)
from .report import render_table_i_report
from .runner import run_eval

__all__ = [
    "build_confusion_matrix",
    "overall_accuracy",
    "per_class_accuracy",
    "per_class_iou",
    "render_table_i_report",
    "run_eval",
    "summarize_metrics",
]
