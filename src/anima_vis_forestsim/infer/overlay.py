"""Palette rendering helpers for qualitative ForestSim outputs."""

from __future__ import annotations

import numpy as np


def colorize(mask: np.ndarray, palette: list[tuple[int, int, int]] | tuple[tuple[int, int, int], ...]) -> np.ndarray:
    """Map a class mask onto an RGB palette."""

    mask_int = np.asarray(mask, dtype=np.int64)
    rgb = np.zeros((*mask_int.shape, 3), dtype=np.uint8)
    for class_idx, color in enumerate(palette):
        rgb[mask_int == class_idx] = color
    return rgb


def blend_overlay(image_rgb: np.ndarray, overlay_rgb: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    """Blend an RGB image with a colorized mask."""

    image = np.asarray(image_rgb, dtype=np.float32)
    overlay = np.asarray(overlay_rgb, dtype=np.float32)
    blended = ((1.0 - alpha) * image) + (alpha * overlay)
    return np.clip(blended, 0, 255).astype(np.uint8)
