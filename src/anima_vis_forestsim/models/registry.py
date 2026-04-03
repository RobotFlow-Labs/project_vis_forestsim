"""Paper benchmark registry sourced from the local Table I manifest."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib

from .families import FAMILY_SPECS, BenchmarkFamily

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PAPER_TABLE_PATH = PROJECT_ROOT / "configs" / "benchmarks" / "paper_table.toml"


@dataclass(frozen=True)
class ModelSpec:
    """Single ForestSim paper-row specification."""

    model_id: str
    label: str
    family: str
    backbone: str
    decoder: str
    pretrained_source: str
    config_path: str
    checkpoint_name: str
    paper_miou: float
    paper_aacc: float
    paper_macc: float

    @property
    def family_spec(self) -> BenchmarkFamily:
        return FAMILY_SPECS[self.family]


def load_paper_table(path: str | Path = DEFAULT_PAPER_TABLE_PATH) -> dict[str, ModelSpec]:
    """Load the local paper benchmark manifest."""

    manifest_path = Path(path)
    if not manifest_path.is_absolute():
        manifest_path = PROJECT_ROOT / manifest_path

    with manifest_path.open("rb") as handle:
        raw = tomllib.load(handle)

    table: dict[str, ModelSpec] = {}
    for model_id, payload in raw.items():
        table[model_id] = ModelSpec(
            model_id=model_id,
            label=payload["label"],
            family=payload["family"],
            backbone=payload["backbone"],
            decoder=payload["decoder"],
            pretrained_source=payload["pretrained_source"],
            config_path=payload["config_path"],
            checkpoint_name=payload["checkpoint_name"],
            paper_miou=float(payload["paper_miou"]),
            paper_aacc=float(payload["paper_aacc"]),
            paper_macc=float(payload["paper_macc"]),
        )
    return table


PAPER_TABLE = load_paper_table()


def get_model_spec(model_id: str) -> ModelSpec:
    """Return a paper benchmark row by stable model ID."""

    try:
        return PAPER_TABLE[model_id]
    except KeyError as exc:
        valid = ", ".join(sorted(PAPER_TABLE))
        raise KeyError(f"Unknown model_id '{model_id}'. Valid model IDs: {valid}") from exc
