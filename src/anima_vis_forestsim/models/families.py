"""Architecture-family defaults used to patch the paper benchmark configs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkFamily:
    """Family-level training defaults normalized out of the reference repo."""

    family: str
    optimizer: str
    scheduler: str
    max_iters: int
    crop_size: tuple[int, int]
    batch_size: int


FAMILY_SPECS: dict[str, BenchmarkFamily] = {
    "pspnet": BenchmarkFamily(
        family="pspnet",
        optimizer="sgd",
        scheduler="poly_40k",
        max_iters=40_000,
        crop_size=(512, 512),
        batch_size=4,
    ),
    "deeplabv3": BenchmarkFamily(
        family="deeplabv3",
        optimizer="sgd",
        scheduler="poly_40k",
        max_iters=40_000,
        crop_size=(512, 512),
        batch_size=4,
    ),
    "deeplabv3plus": BenchmarkFamily(
        family="deeplabv3plus",
        optimizer="sgd",
        scheduler="poly_40k",
        max_iters=40_000,
        crop_size=(512, 512),
        batch_size=4,
    ),
    "segformer": BenchmarkFamily(
        family="segformer",
        optimizer="adamw",
        scheduler="linear_warmup_poly_160k",
        max_iters=160_000,
        crop_size=(512, 512),
        batch_size=2,
    ),
    "mask2former": BenchmarkFamily(
        family="mask2former",
        optimizer="adamw",
        scheduler="poly_160k",
        max_iters=160_000,
        crop_size=(512, 512),
        batch_size=2,
    ),
}
