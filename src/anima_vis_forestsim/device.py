"""Runtime device selection for local MLX and remote CUDA execution."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class DeviceInfo:
    """Resolved compute backend information."""

    backend: str
    accelerator: str
    torch_device: str | None


def _detect_backend() -> DeviceInfo:
    requested = os.environ.get("ANIMA_BACKEND", "auto").strip().lower()

    if requested in {"mlx", "auto"}:
        try:
            import mlx.core as mx  # type: ignore
        except ImportError:
            pass
        else:
            return DeviceInfo(backend="mlx", accelerator=str(mx.default_device()), torch_device=None)

    try:
        import torch
    except ImportError:
        return DeviceInfo(backend="cpu", accelerator="cpu", torch_device=None)

    if requested in {"cuda", "auto"} and torch.cuda.is_available():
        return DeviceInfo(backend="cuda", accelerator=torch.cuda.get_device_name(0), torch_device="cuda")

    if requested == "cuda":
        return DeviceInfo(backend="cpu", accelerator="cpu", torch_device="cpu")

    if requested not in {"auto", "cpu"}:
        return DeviceInfo(backend="cpu", accelerator="cpu", torch_device="cpu")

    return DeviceInfo(backend="cpu", accelerator="cpu", torch_device="cpu")


def get_device_info() -> DeviceInfo:
    """Return the resolved backend for the current runtime."""

    return _detect_backend()
