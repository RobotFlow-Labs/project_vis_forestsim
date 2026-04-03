# VIS-FORESTSIM — Execution Ledger

Resume rule: Read this file completely before writing code.
This project covers exactly one paper: ForestSim: A Synthetic Benchmark for Intelligent Vehicle Perception in Unstructured Forest Environments.

## 1. Working Rules
- Work only inside `project_vis_forestsim/`
- Prefix commits with `[VIS-FORESTSIM]`
- Stage only `project_vis_forestsim/` files
- Verify ontology, split logic, and config class counts before training anything

## 2. The Paper
- **Title**: ForestSim: A Synthetic Benchmark for Intelligent Vehicle Perception in Unstructured Forest Environments
- **ArXiv**: 2603.27923
- **Link**: https://arxiv.org/abs/2603.27923
- **Repo**: https://github.com/pragatwagle/ForestSim
- **Compute**: GPU-NEED
- **Verification status**: ArXiv ID ✅ | Repo ✅ | Paper read ✅ | Benchmark table extracted ✅

## 3. Current Status
- **Date**: 2026-04-03
- **Phase**: PRD scaffolded
- **MVP Readiness**: 15%
- **Accomplished**:
  1. Local paper PDF reviewed
  2. Reference repository inspected
  3. `ASSETS.md`, `PIPELINE_MAP.md`, `prds/`, and `tasks/` plan created
- **TODO**:
  1. Stage ForestSim raw dataset locally
  2. Stage pretrained checkpoints locally
  3. Implement PRD-01 foundation and ontology reconciliation
  4. Run the reference benchmark path on at least one paper model
  5. Begin Table I reproduction in ANIMA code
- **Blockers**:
  1. Dataset archive not yet staged locally
  2. Pretrained checkpoints not yet staged locally

## 4. Datasets

| Dataset | Size | URL | Format | Phase Needed |
|---------|------|-----|--------|-------------|
| ForestSim raw | 2094 pairs | https://vailforestsim.github.io/ | RGB PNG + segmentation PNG | Phase 1 |
| ForestSim 24-class processed | derived | local conversion | MMSeg-style images + masks | Phase 1 |
| ForestSim 6-class grouped | derived | local conversion | traversability masks | Phase 1 |

Shared storage target:

`/mnt/forge-data/datasets/vision/forestsim/`

## 5. Hardware
- Mac Studio M-series: local editing and smoke-test inference
- Remote CUDA box or cluster: benchmark training and full reproduction
- Paper training reference: 4 nodes x 4 NVIDIA A100 GPUs

## 6. Session Log

| Date | Agent | What Happened |
|------|-------|---------------|
| 2026-04-03 | Codex | Read paper and reference repo, generated PRD suite and tasks |
