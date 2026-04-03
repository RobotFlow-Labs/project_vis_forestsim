# PRD-07: Production Validation & Artifact Packaging

> Module: VIS-FORESTSIM | Priority: P2  
> Depends on: PRD-04, PRD-05, PRD-06  
> Status: ⬜ Not started

## Objective

Package the chosen ForestSim checkpoint and validation evidence into deployable ANIMA artifacts with reproducibility, fallback, and publication metadata.

## Context (from paper)

The paper concludes that ForestSim is a robust baseline for advancing intelligent vehicle research. The production PRD turns that claim into shippable ANIMA artifacts with benchmark traceability.

**Paper reference**: §VII

## Acceptance Criteria

- [ ] Export pipeline can package the selected checkpoint and metadata bundle.
- [ ] Production validation report links checkpoint, ontology, split, and reproduced metrics.
- [ ] Runtime supports graceful failure for missing checkpoints, unsupported ontology, or absent CUDA.
- [ ] Artifact manifest is suitable for model registry or Hugging Face publication.
- [ ] Test: `uv run pytest tests/test_artifact_manifest.py tests/test_runtime_fallbacks.py -v` passes.

## Files to Create

| File | Purpose | Paper Ref | Est. Lines |
|------|---------|-----------|-----------|
| `src/anima_vis_forestsim/export.py` | artifact packaging | §VII | ~140 |
| `src/anima_vis_forestsim/runtime_checks.py` | fallback and environment checks | — | ~100 |
| `reports/forestsim_benchmark_template.md` | production validation report template | Table I, §VII | ~80 |
| `tests/test_artifact_manifest.py` | manifest tests | — | ~70 |
| `tests/test_runtime_fallbacks.py` | fallback tests | — | ~80 |

## Architecture Detail (from paper)

### Inputs

`checkpoint_path: str`  
`benchmark_report: Path`  
`runtime_env: dict`

### Outputs

`artifact_manifest.json`  
`production_report.md`  
`export_bundle.tar.gz`

### Algorithm

```python
# Paper §VII -- turn the benchmark into a reusable baseline artifact
def build_artifact_manifest(spec, metrics, checkpoint_path):
    return {
        "module": "VIS-FORESTSIM",
        "checkpoint": checkpoint_path,
        "paper_table_target": spec.paper_metrics,
        "observed_metrics": metrics,
    }
```

## Dependencies

```toml
orjson = ">=3.10"
platformdirs = ">=4.2"
```

## Data Requirements

| Asset | Size | Path | Download |
|------|------|------|----------|
| benchmark report | small | `reports/forestsim_benchmark.md` | local output |
| selected model checkpoint | variable | `/mnt/forge-data/models/vision/...` | staged locally |

## Test Plan

```bash
uv run pytest tests/test_artifact_manifest.py tests/test_runtime_fallbacks.py -v
```

## References

- Paper: §VII “Conclusion”
- Depends on: PRD-04, PRD-05, PRD-06
- Feeds into: deployment and registry publication
