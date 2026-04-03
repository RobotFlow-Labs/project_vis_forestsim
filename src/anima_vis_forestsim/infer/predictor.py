"""Checkpoint-aware predictor with explicit prebuild fallback behavior."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from ..config import ForestSimSettings, load_settings
from ..data.ontology import resolve_ontology
from ..models.checkpoints import resolve_checkpoint_spec


@dataclass(frozen=True)
class PredictionResult:
    """Structured inference output."""

    checkpoint_id: str
    ontology: str
    logits: np.ndarray
    mask: np.ndarray
    overlay: np.ndarray
    used_stub: bool
    checkpoint_exists: bool
    warning: str | None


class ForestSimPredictor:
    """Prebuild predictor contract for local smoke tests and service plumbing."""

    def __init__(self, settings: ForestSimSettings | None = None, image_size: tuple[int, int] = (512, 512)):
        self.settings = settings or load_settings()
        self.image_size = image_size

    def preprocess(self, image_rgb: np.ndarray) -> np.ndarray:
        """Resize input RGB imagery onto the benchmark crop size."""

        image = np.asarray(image_rgb, dtype=np.uint8)
        return cv2.resize(image, self.image_size, interpolation=cv2.INTER_LINEAR)

    def _stub_logits(self, image_rgb: np.ndarray, num_classes: int) -> np.ndarray:
        """Deterministic fallback logits used before real checkpoint loading exists."""

        image = image_rgb.astype(np.float32) / 255.0
        red = image[..., 0]
        green = image[..., 1]
        blue = image[..., 2]
        gray = ((red + green + blue) / 3.0).astype(np.float32)
        sobel_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        edges = np.sqrt((sobel_x**2) + (sobel_y**2))

        features = np.stack(
            [
                red,
                green,
                blue,
                gray,
                edges,
                1.0 - gray,
            ],
            axis=0,
        )

        logits = np.zeros((1, num_classes, *gray.shape), dtype=np.float32)
        for class_idx in range(num_classes):
            feature = features[class_idx % features.shape[0]]
            offset = (class_idx + 1) / max(num_classes, 1)
            logits[0, class_idx] = feature + offset
        return logits

    def predict(
        self,
        image_rgb: np.ndarray,
        checkpoint_id: str = "m12",
        ontology: str = "forestsim24",
    ) -> PredictionResult:
        """Return raw logits, mask, and overlay for the requested benchmark row."""

        ontology_spec = resolve_ontology(ontology)
        checkpoint = resolve_checkpoint_spec(checkpoint_id, self.settings.checkpoint_root)
        resized = self.preprocess(image_rgb)

        warning = None
        if checkpoint.exists:
            warning = (
                "Checkpoint was found, but executable model loading is not implemented in the prebuild scaffold. "
                "Returning deterministic stub logits."
            )
        else:
            warning = (
                f"Checkpoint '{checkpoint.path.name}' is not staged under '{checkpoint.path.parent}'. "
                "Returning deterministic stub logits."
            )

        logits = self._stub_logits(resized, ontology_spec.num_classes)
        mask = logits.argmax(axis=1)[0].astype(np.uint8)

        from .overlay import colorize

        overlay = colorize(mask, ontology_spec.palette)
        return PredictionResult(
            checkpoint_id=checkpoint_id,
            ontology=ontology_spec.name,
            logits=logits,
            mask=mask,
            overlay=overlay,
            used_stub=True,
            checkpoint_exists=checkpoint.exists,
            warning=warning,
        )
