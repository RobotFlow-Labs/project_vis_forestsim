"""Request and response schemas for the local inference service."""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    module: str
    backend: str
    python: str


class MetadataResponse(BaseModel):
    codename: str
    default_ontology: str
    available_models: list[str]
    cuda_dependencies_enabled: bool
    mlx_dependencies_enabled: bool


class SegmentPathRequest(BaseModel):
    image_path: str = Field(..., description="Local filesystem path to an RGB image.")
    checkpoint_id: str = "m12"
    ontology: str = "forestsim24"


class SegmentResponse(BaseModel):
    checkpoint_id: str
    ontology: str
    used_stub: bool
    checkpoint_exists: bool
    warning: str | None
    mask_png_base64: str
    overlay_png_base64: str
