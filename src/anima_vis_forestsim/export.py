"""Artifact manifest helpers for packaging validated benchmark assets."""

from __future__ import annotations

from pathlib import Path

from .models.registry import get_model_spec


def build_artifact_manifest(
    checkpoint_path: str | Path,
    model_id: str,
    ontology: str,
    observed_metrics: dict[str, float] | None = None,
) -> dict[str, object]:
    """Build an ANIMA-ready artifact manifest payload."""

    spec = get_model_spec(model_id)
    checkpoint = Path(checkpoint_path)
    return {
        "module": "VIS-FORESTSIM",
        "paper": {
            "arxiv": "2603.27923",
            "model_id": model_id,
            "label": spec.label,
        },
        "checkpoint": {
            "path": str(checkpoint),
            "exists": checkpoint.exists(),
            "pretrained_source": spec.pretrained_source,
        },
        "ontology": ontology,
        "paper_metrics": {
            "mIoU": spec.paper_miou,
            "aAcc": spec.paper_aacc,
            "mAcc": spec.paper_macc,
        },
        "observed_metrics": observed_metrics or {},
    }
