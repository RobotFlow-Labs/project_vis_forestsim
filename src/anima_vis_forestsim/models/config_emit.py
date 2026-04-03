"""Emit corrected ANIMA-native config payloads for benchmark rows."""

from __future__ import annotations

from .registry import get_model_spec
from ..data.ontology import OntologySpec


def emit_config(model_id: str, ontology: OntologySpec) -> dict[str, object]:
    """Generate a normalized config bundle for a paper model."""

    spec = get_model_spec(model_id)
    family = spec.family_spec
    return {
        "model_id": spec.model_id,
        "label": spec.label,
        "family": spec.family,
        "backbone": spec.backbone,
        "decoder": spec.decoder,
        "config_path": spec.config_path,
        "crop_size": list(family.crop_size),
        "batch_size": family.batch_size,
        "max_iters": family.max_iters,
        "optimizer": family.optimizer,
        "scheduler": family.scheduler,
        "num_classes": ontology.num_classes,
        "ontology": ontology.name,
        "paper_metrics": {
            "mIoU": spec.paper_miou,
            "aAcc": spec.paper_aacc,
            "mAcc": spec.paper_macc,
        },
    }
