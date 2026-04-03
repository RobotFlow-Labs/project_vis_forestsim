# PRD-04: Evaluation & Table I Reproduction

> Module: VIS-FORESTSIM | Priority: P0  
> Depends on: PRD-01, PRD-02, PRD-03  
> Status: ⬜ Not started

## Objective

Reproduce the paper evaluation protocol and emit a machine-readable comparison against Table I.

## Context (from paper)

The paper’s credibility comes from the benchmark results. ANIMA must therefore reproduce the split protocol and metrics and explain any deltas against the published table.

**Paper reference**: §VI-B, §VI-C, Table I

## Acceptance Criteria

- [ ] Evaluation runner consumes a split manifest and benchmark spec and emits `aAcc`, `mIoU`, and `mAcc`.
- [ ] Report generator compares reproduced metrics against all 13 paper rows.
- [ ] The runner can evaluate a single checkpoint or a batch benchmark sweep.
- [ ] Regression tests validate metric aggregation on deterministic toy masks.
- [ ] Test: `uv run pytest tests/test_metrics.py tests/test_eval_runner.py tests/test_table_i_report.py -v` passes.

## Files to Create

| File | Purpose | Paper Ref | Est. Lines |
|------|---------|-----------|-----------|
| `src/anima_vis_forestsim/eval/metrics.py` | metric wrappers and summaries | §VI-B | ~120 |
| `src/anima_vis_forestsim/eval/runner.py` | evaluation orchestration | §VI-B, §VI-C | ~210 |
| `src/anima_vis_forestsim/eval/report.py` | Table I comparison report | Table I | ~170 |
| `tests/test_metrics.py` | metric unit tests | — | ~80 |
| `tests/test_eval_runner.py` | evaluation pipeline tests | — | ~100 |
| `tests/test_table_i_report.py` | report generation tests | — | ~90 |

## Architecture Detail (from paper)

### Inputs

`pred_mask: Tensor[N, 512, 512]`  
`target_mask: Tensor[N, 512, 512]`  
`paper_targets: dict[str, float]`

### Outputs

`MetricSummary(aAcc, mIoU, mAcc)`  
`TableIRow(model_id, reported_mIoU, observed_mIoU, delta_mIoU)`  
`benchmark_report.md`

### Algorithm

```python
# Paper §VI-B -- Mean IoU and pixel accuracy
def summarize_metrics(confusion: np.ndarray) -> dict[str, float]:
    iou = per_class_iou(confusion)
    acc = per_class_accuracy(confusion)
    return {
        "aAcc": overall_accuracy(confusion),
        "mIoU": float(np.nanmean(iou)),
        "mAcc": float(np.nanmean(acc)),
    }
```

## Dependencies

```toml
pandas = ">=2.2"
numpy = ">=1.26"
tabulate = ">=0.9"
```

## Data Requirements

| Asset | Size | Path | Download |
|------|------|------|----------|
| benchmark split manifest | small | `/mnt/forge-data/datasets/vision/forestsim/.../train.txt` and `test.txt` | staged locally |
| paper metric table | small | `configs/benchmarks/paper_table.toml` | local |

## Test Plan

```bash
uv run pytest tests/test_metrics.py tests/test_eval_runner.py tests/test_table_i_report.py -v
```

## References

- Paper: §VI-B “Data Split, Training, and Evaluation Metrics”
- Paper: §VI-C “Analysis and Experimental Evaluation”
- Paper: Table I
- Reference impl: `repositories/ForestSim/testresults/forestsim/`
- Depends on: PRD-01, PRD-02, PRD-03
- Feeds into: PRD-07
