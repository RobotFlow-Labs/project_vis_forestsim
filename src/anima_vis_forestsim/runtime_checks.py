"""Runtime validation helpers for local Mac and remote CUDA deployments."""

from __future__ import annotations

from .config import ForestSimSettings, load_settings
from .data.ontology import resolve_ontology
from .device import get_device_info
from .models.checkpoints import resolve_checkpoint_spec


def validate_runtime(
    settings: ForestSimSettings | None = None,
    checkpoint_id: str = "m12",
) -> list[str]:
    """Return non-fatal runtime warnings for the current environment."""

    resolved_settings = settings or load_settings()
    warnings: list[str] = []
    device = get_device_info()

    if resolved_settings.cuda_dependencies_enabled and device.backend != "cuda":
        warnings.append(
            "CUDA dependencies are enabled in config, but the active runtime is not CUDA."
        )

    if resolved_settings.mlx_dependencies_enabled and device.backend not in {"mlx", "cuda"}:
        warnings.append("Neither MLX nor CUDA acceleration is active; running on CPU fallback.")

    checkpoint = resolve_checkpoint_spec(checkpoint_id, resolved_settings.checkpoint_root)
    if not checkpoint.exists:
        warnings.append(f"Checkpoint not staged: {checkpoint.path}")

    try:
        resolve_ontology(resolved_settings.default_ontology)
    except KeyError as exc:
        warnings.append(str(exc))

    return warnings
