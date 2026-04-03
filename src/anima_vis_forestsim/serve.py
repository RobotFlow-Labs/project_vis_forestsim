"""Minimal uvicorn entry surface for local and container serving."""

from __future__ import annotations

from .api.app import app

__all__ = ["app"]
