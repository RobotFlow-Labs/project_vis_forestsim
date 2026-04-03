# VIS-FORESTSIM PRD Index

## Build Order

1. [PRD-01-foundation.md](PRD-01-foundation.md)
2. [PRD-02-core-model.md](PRD-02-core-model.md)
3. [PRD-03-inference.md](PRD-03-inference.md)
4. [PRD-04-evaluation.md](PRD-04-evaluation.md)
5. [PRD-05-api-docker.md](PRD-05-api-docker.md)
6. [PRD-06-ros2-integration.md](PRD-06-ros2-integration.md)
7. [PRD-07-production.md](PRD-07-production.md)

## Notes

- This module reproduces a benchmark paper, so fidelity to data processing and configuration matters more than inventing new layers.
- PRD-01 must resolve the paper/repo class-count and naming drift before any benchmark claim is trusted.
- PRD-04 is the paper-truth gate: if Table I cannot be recreated or explained, later deployment work is not valid.
