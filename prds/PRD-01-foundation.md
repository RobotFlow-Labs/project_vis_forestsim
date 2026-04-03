# PRD-01: Foundation & Reconciliation

> Module: VIS-FORESTSIM | Priority: P0  
> Depends on: None  
> Status: ⬜ Not started

## Objective

Create the ANIMA-native package, config, ontology, and asset contracts that make the ForestSim benchmark reproducible instead of ambiguous.

## Context (from paper)

ForestSim is primarily a data and benchmark contribution. The paper’s core promise is a synthetic off-road segmentation benchmark with consistent pixel-wise labels across a defined set of classes, so the first implementation requirement is dataset and configuration correctness.

**Paper reference**: §IV-D, §V, §VI-B  
Key grounding:
- “each environment underwent manual curation”
- “20 distinct object classes”
- “split randomly into training (90%) and testing (10%) sets”

## Acceptance Criteria

- [ ] `src/anima_vis_forestsim/` exists and replaces the current placeholder package target in the build plan.
- [ ] The module exposes a canonical ontology contract for `forestsim24` and `forestsim6`.
- [ ] The package defines explicit compatibility aliases for `forestsim`, `forestsim_all`, and `vail_all`.
- [ ] Dataset root, split files, and checkpoint paths resolve through typed settings.
- [ ] A reconciliation report documents the 20-class paper claim vs the 24-class / 6-class repo variants.
- [ ] Test: `uv run pytest tests/test_config.py tests/test_ontology.py -v` passes.

## Files to Create

| File | Purpose | Paper Ref | Est. Lines |
|------|---------|-----------|-----------|
| `src/anima_vis_forestsim/__init__.py` | canonical package export | — | ~20 |
| `src/anima_vis_forestsim/config.py` | typed settings and path resolution | §VI-B | ~140 |
| `src/anima_vis_forestsim/data/ontology.py` | 24-class and 6-class mappings | §V | ~180 |
| `src/anima_vis_forestsim/data/manifest.py` | dataset and checkpoint manifest types | §IV-D, §VI-B | ~120 |
| `tests/test_config.py` | settings validation | — | ~70 |
| `tests/test_ontology.py` | ontology and alias tests | — | ~90 |
| `configs/default.toml` | default runtime settings | — | ~80 |

## Architecture Detail (from paper)

### Inputs

`rgb_path: str`  
`segmentation_path: str`  
`split_manifest: dict[str, list[str]]`

### Outputs

`ForestSimSettings`  
`OntologySpec(name, num_classes, palette, aliases)`  
`AssetManifest(datasets, checkpoints, paper_metrics)`

### Algorithm

```python
# Paper §§IV-VI -- dataset preparation and benchmark protocol
from dataclasses import dataclass


@dataclass(frozen=True)
class OntologySpec:
    name: str
    num_classes: int
    palette: list[tuple[int, int, int]]
    aliases: tuple[str, ...]


def resolve_ontology(name: str) -> OntologySpec:
    normalized = name.replace("-", "_").lower()
    if normalized in {"forestsim24", "forestsim_all", "vail_all"}:
        return FORESTSIM24
    if normalized in {"forestsim6", "forestsim_group6"}:
        return FORESTSIM6
    raise KeyError(name)
```

## Dependencies

```toml
pydantic = ">=2.7"
pydantic-settings = ">=2.2"
tomli = { version = ">=2.0", markers = "python_version < '3.11'" }
```

## Data Requirements

| Asset | Size | Path | Download |
|------|------|------|----------|
| ForestSim raw dataset | 2094 pairs | `/mnt/forge-data/datasets/vision/forestsim/raw/` | https://vailforestsim.github.io/ |
| benchmark manifest | small | `ASSETS.md` mirrored into runtime JSON | local |

## Test Plan

```bash
uv run pytest tests/test_config.py tests/test_ontology.py -v
uv run ruff check src/ tests/
```

## References

- Paper: §IV-D “Data Processing and Statistics”
- Paper: §V “Annotation Statistics and Ontology”
- Paper: §VI-B “Data Split, Training, and Evaluation Metrics”
- Reference impl: `repositories/ForestSim/mmseg/datasets/forestsim.py`
- Reference impl: `repositories/ForestSim/mmseg/datasets/forestsim_group6.py`
- Depends on: None
- Feeds into: PRD-02, PRD-03, PRD-04
