"""Checkpoint resolution for local and remote ForestSim artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .registry import ModelSpec, get_model_spec


@dataclass(frozen=True)
class ResolvedCheckpoint:
    """Resolved checkpoint location and availability status."""

    model: ModelSpec
    path: Path
    exists: bool


def _normalize_root(root: str | Path) -> Path:
    path = Path(root)
    return path.expanduser().resolve() if path.exists() else path.expanduser()


def resolve_checkpoint(model_id: str, root: str | Path) -> Path:
    """Resolve a model checkpoint path under a checkpoint root."""

    spec = get_model_spec(model_id)
    return _normalize_root(root) / spec.family / spec.checkpoint_name


def resolve_checkpoint_spec(model_id: str, root: str | Path) -> ResolvedCheckpoint:
    """Return path resolution and existence information for a model checkpoint."""

    spec = get_model_spec(model_id)
    path = resolve_checkpoint(model_id, root)
    return ResolvedCheckpoint(model=spec, path=path, exists=path.exists())
