# PRD-05: API & Docker

> Module: VIS-FORESTSIM | Priority: P1  
> Depends on: PRD-03  
> Status: ⬜ Not started

## Objective

Expose VIS-FORESTSIM inference behind a stable API and container runtime that can be deployed without importing the research repository.

## Context (from paper)

The paper itself does not define a serving interface, but the benchmark is only useful in ANIMA if a chosen checkpoint can be consumed programmatically by other modules.

**Paper reference**: derived from §VI-C outputs and Table I best models

## Acceptance Criteria

- [ ] FastAPI exposes health, metadata, and segmentation endpoints.
- [ ] API accepts RGB image uploads or file-path requests and returns mask plus overlay metadata.
- [ ] Docker image builds a CPU-capable inference service with optional CUDA extras.
- [ ] Compose or run instructions document checkpoint and dataset mounts.
- [ ] Test: `uv run pytest tests/test_api.py -v` passes.

## Files to Create

| File | Purpose | Paper Ref | Est. Lines |
|------|---------|-----------|-----------|
| `src/anima_vis_forestsim/api/schemas.py` | request/response models | — | ~90 |
| `src/anima_vis_forestsim/api/app.py` | FastAPI service | derived from §VI-C outputs | ~160 |
| `Dockerfile` | runtime image | — | ~45 |
| `docker-compose.yml` | local serving harness | — | ~40 |
| `tests/test_api.py` | API contract tests | — | ~90 |

## Architecture Detail (from paper)

### Inputs

`multipart/form-data` image  
`checkpoint_id: str`  
`ontology: str`

### Outputs

`mask_png: bytes`  
`overlay_png: bytes`  
`metrics_hint: {"paper_mIoU": float | null}`

### Algorithm

```python
# Derived from paper benchmark outputs
@app.post("/segment")
def segment_image(req: SegmentRequest) -> SegmentResponse:
    logits, mask, overlay = predictor.predict(req.image, req.checkpoint_id, req.ontology)
    return SegmentResponse.from_arrays(mask=mask, overlay=overlay)
```

## Dependencies

```toml
fastapi = ">=0.111"
uvicorn = ">=0.30"
python-multipart = ">=0.0.9"
```

## Data Requirements

| Asset | Size | Path | Download |
|------|------|------|----------|
| selected checkpoint | variable | `/models/forestsim/` mounted in container | staged locally |

## Test Plan

```bash
uv run pytest tests/test_api.py -v
docker build -t vis-forestsim:dev .
```

## References

- Paper: §VI-C output expectations
- Depends on: PRD-03
- Feeds into: PRD-06, PRD-07
