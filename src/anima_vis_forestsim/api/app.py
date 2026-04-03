"""FastAPI application wrapping the local predictor contract."""

from __future__ import annotations

from base64 import b64encode
from pathlib import Path

import cv2
from fastapi import FastAPI, HTTPException, UploadFile

from ..config import load_settings
from ..device import get_device_info
from ..infer.predictor import ForestSimPredictor
from ..models.registry import PAPER_TABLE
from .schemas import HealthResponse, MetadataResponse, SegmentPathRequest, SegmentResponse

app = FastAPI(title="VIS-FORESTSIM", version="0.1.0")


def _encode_png(image: object) -> str:
    success, encoded = cv2.imencode(".png", image)
    if not success:
        raise RuntimeError("Failed to encode PNG response.")
    return b64encode(encoded.tobytes()).decode("ascii")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = load_settings()
    device = get_device_info()
    return HealthResponse(
        status="ok",
        module=settings.codename,
        backend=device.backend,
        python=settings.python_version,
    )


@app.get("/metadata", response_model=MetadataResponse)
def metadata() -> MetadataResponse:
    settings = load_settings()
    return MetadataResponse(
        codename=settings.codename,
        default_ontology=settings.default_ontology,
        available_models=sorted(PAPER_TABLE),
        cuda_dependencies_enabled=settings.cuda_dependencies_enabled,
        mlx_dependencies_enabled=settings.mlx_dependencies_enabled,
    )


@app.post("/segment/path", response_model=SegmentResponse)
def segment_from_path(request: SegmentPathRequest) -> SegmentResponse:
    image_path = Path(request.image_path)
    image_bgr = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise HTTPException(status_code=404, detail=f"Could not read image at {image_path}")

    predictor = ForestSimPredictor()
    result = predictor.predict(
        image_rgb=cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB),
        checkpoint_id=request.checkpoint_id,
        ontology=request.ontology,
    )
    return SegmentResponse(
        checkpoint_id=result.checkpoint_id,
        ontology=result.ontology,
        used_stub=result.used_stub,
        checkpoint_exists=result.checkpoint_exists,
        warning=result.warning,
        mask_png_base64=_encode_png(result.mask),
        overlay_png_base64=_encode_png(cv2.cvtColor(result.overlay, cv2.COLOR_RGB2BGR)),
    )


@app.post("/segment/upload", response_model=SegmentResponse)
async def segment_upload(
    file: UploadFile,
    checkpoint_id: str = "m12",
    ontology: str = "forestsim24",
) -> SegmentResponse:
    payload = await file.read()
    image_bgr = cv2.imdecode(cv2.UMat(payload), cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise HTTPException(status_code=400, detail="Upload payload is not a valid image.")

    predictor = ForestSimPredictor()
    result = predictor.predict(
        image_rgb=cv2.cvtColor(image_bgr.get(), cv2.COLOR_BGR2RGB),
        checkpoint_id=checkpoint_id,
        ontology=ontology,
    )
    return SegmentResponse(
        checkpoint_id=result.checkpoint_id,
        ontology=result.ontology,
        used_stub=result.used_stub,
        checkpoint_exists=result.checkpoint_exists,
        warning=result.warning,
        mask_png_base64=_encode_png(result.mask),
        overlay_png_base64=_encode_png(cv2.cvtColor(result.overlay, cv2.COLOR_RGB2BGR)),
    )
