# PRD-03: Inference & Visualization

> Module: VIS-FORESTSIM | Priority: P1  
> Depends on: PRD-01, PRD-02  
> Status: ⬜ Not started

## Objective

Provide a checkpoint-backed predictor that turns RGB inputs into segmentation masks, overlays, and benchmark-friendly metadata.

## Context (from paper)

The paper uses trained models to produce predictions that are visually compared against ground truth in Fig. 7 and Fig. 8. A usable ANIMA module needs an inference surface that reproduces those outputs without retraining.

**Paper reference**: §VI-C, Fig. 7, Fig. 8

## Acceptance Criteria

- [ ] Predictor loads any supported paper checkpoint through the registry.
- [ ] Preprocessing matches the benchmark crop/resize path.
- [ ] The predictor returns raw logits, class masks, and color overlays.
- [ ] A CLI accepts image paths and emits mask PNG plus JSON metadata.
- [ ] Test: `uv run pytest tests/test_predictor.py tests/test_cli.py -v` passes.

## Files to Create

| File | Purpose | Paper Ref | Est. Lines |
|------|---------|-----------|-----------|
| `src/anima_vis_forestsim/models/checkpoints.py` | checkpoint resolution | §VI-A | ~120 |
| `src/anima_vis_forestsim/infer/predictor.py` | inference engine | §VI-C | ~220 |
| `src/anima_vis_forestsim/infer/overlay.py` | palette rendering | Fig. 7, Fig. 8 | ~110 |
| `src/anima_vis_forestsim/infer/cli.py` | command line entry | — | ~130 |
| `tests/test_predictor.py` | predictor contract tests | — | ~100 |
| `tests/test_cli.py` | CLI smoke tests | — | ~70 |

## Architecture Detail (from paper)

### Inputs

`image: Tensor[1, 3, H, W]`  
`checkpoint_id: str`  
`ontology: str`

### Outputs

`logits: Tensor[1, C, 512, 512]`  
`mask: Tensor[1, 512, 512]`  
`overlay_rgb: Tensor[1, 512, 512, 3]`

### Algorithm

```python
# Paper §VI-C -- trained models make predictions on the randomized test set
class ForestSimPredictor:
    def __init__(self, registry, device):
        self.registry = registry
        self.device = device

    def predict(self, image: np.ndarray, checkpoint_id: str, ontology: str):
        spec = self.registry.resolve(checkpoint_id, ontology)
        batch = preprocess(image, crop_size=(512, 512))
        logits = self._forward(spec, batch)
        mask = logits.argmax(axis=1)
        overlay = colorize(mask, palette=spec.palette)
        return logits, mask, overlay
```

## Dependencies

```toml
numpy = ">=1.26"
opencv-python = ">=4.9"
pillow = ">=10.0"
typer = ">=0.12"
```

## Data Requirements

| Asset | Size | Path | Download |
|------|------|------|----------|
| supported checkpoint | variable | `/mnt/forge-data/models/vision/...` | see `ASSETS.md` |
| sample RGB fixture | small | `tests/fixtures/forestsim_sample.png` | local fixture |

## Test Plan

```bash
uv run pytest tests/test_predictor.py tests/test_cli.py -v
```

## References

- Paper: §VI-C “Analysis and Experimental Evaluation”
- Paper: Fig. 7, Fig. 8
- Reference impl: `repositories/ForestSim/tools/test.py`
- Depends on: PRD-01, PRD-02
- Feeds into: PRD-05, PRD-06, PRD-07
