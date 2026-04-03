# PRD-02: Core Benchmark Stack

> Module: VIS-FORESTSIM | Priority: P0  
> Depends on: PRD-01  
> Status: ⬜ Not started

## Objective

Implement the benchmark-family registry and training configuration layer that reproduces the 13 paper models with corrected class counts and dataset bindings.

## Context (from paper)

The paper evaluates a set of modern encoder-decoder families rather than proposing a novel network. The ANIMA implementation must preserve those exact benchmark families and their published recipes.

**Paper reference**: §VI-A, Table I  
Key grounding:
- “evaluation representative modern segmentation architectures”
- “encoder-decoder pattern”
- “trained using AdamW optimizer and PolyLR scheduler”

## Acceptance Criteria

- [ ] A benchmark registry resolves all 13 paper models by stable ID.
- [ ] Model family descriptors capture backbone, decoder, pretrained source, ontology, and scheduler.
- [ ] The registry patches invalid repo head sizes (`150`, `171`) to ontology-correct class counts.
- [ ] Config emitters can generate a runnable config bundle for PSPNet, DeepLabV3, DeepLabV3+, SegFormer, and Mask2Former families.
- [ ] The training layer supports both 24-class and 6-class ontology targets.
- [ ] Test: `uv run pytest tests/test_model_registry.py tests/test_benchmark_configs.py -v` passes.

## Files to Create

| File | Purpose | Paper Ref | Est. Lines |
|------|---------|-----------|-----------|
| `src/anima_vis_forestsim/models/registry.py` | 13-model paper registry | Table I | ~180 |
| `src/anima_vis_forestsim/models/families.py` | benchmark family dataclasses | §VI-A | ~150 |
| `src/anima_vis_forestsim/models/config_emit.py` | ANIMA-to-mmseg config generation | §VI-A, §VI-B | ~220 |
| `configs/benchmarks/paper_table.toml` | paper model list and target metrics | Table I | ~140 |
| `tests/test_model_registry.py` | registry fidelity tests | — | ~90 |
| `tests/test_benchmark_configs.py` | config emission tests | — | ~110 |

## Architecture Detail (from paper)

### Inputs

`image: Tensor[B, 3, 512, 512]`  
`ontology: Literal["forestsim24", "forestsim6"]`  
`model_id: Literal["m1", ..., "m13"]`

### Outputs

`BenchmarkSpec`  
`ResolvedBenchmarkConfig`  
`logits: Tensor[B, C, 512, 512]`

### Algorithm

```python
# Paper §VI-A / Table I -- benchmark families
class BenchmarkSpec(TypedDict):
    model_id: str
    family: str
    backbone: str
    decoder: str
    pretrained: str
    scheduler: str
    max_iters: int


def build_benchmark_spec(model_id: str, ontology: OntologySpec) -> BenchmarkSpec:
    spec = PAPER_TABLE[model_id]
    spec["num_classes"] = ontology.num_classes
    return spec
```

## Dependencies

```toml
mmengine = ">=0.8"
mmcv-lite = ">=2.0"
mmsegmentation = ">=1.2"
mmdet = ">=3.2"
```

## Data Requirements

| Asset | Size | Path | Download |
|------|------|------|----------|
| benchmark config table | small | `configs/benchmarks/paper_table.toml` | local |
| pretrained checkpoints | variable | `/mnt/forge-data/models/vision/` | see `ASSETS.md` |

## Test Plan

```bash
uv run pytest tests/test_model_registry.py tests/test_benchmark_configs.py -v
uv run ruff check src/ tests/
```

## References

- Paper: §VI-A “Baselines and Experimental Setups”
- Paper: Table I
- Reference impl: `repositories/ForestSim/configs/`
- Depends on: PRD-01
- Feeds into: PRD-03, PRD-04
