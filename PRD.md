# VIS-FORESTSIM: ForestSim — Implementation PRD
## ANIMA Wave-7 Vision Module

**Status:** Planning complete  
**Version:** 0.2  
**Date:** 2026-04-03  
**Paper:** ForestSim: A Synthetic Benchmark for Intelligent Vehicle Perception in Unstructured Forest Environments  
**Paper Link:** https://arxiv.org/abs/2603.27923  
**Repo:** https://github.com/pragatwagle/ForestSim  
**Functional Name:** `VIS-FORESTSIM`  
**Package Target:** `anima_vis_forestsim`  
**Stack:** ANIMA / MMSegmentation-compatible benchmark reproduction

## 1. Executive Summary

ForestSim is a dataset-and-benchmark paper rather than a new architecture paper. The ANIMA implementation therefore centers on reproducible dataset processing, benchmark configuration, inference packaging, and deployment surfaces for the strongest published checkpoints. The module must reproduce the paper’s dataset conventions and Table I benchmark families while correcting the manuscript-to-repository drift already visible in the reference codebase.

## 2. Paper Verification Status

- [x] ArXiv ID verified
- [x] Reference repository present locally
- [x] Paper read completely
- [x] Paper benchmark table extracted
- [ ] Dataset archive staged locally
- [ ] Pretrained checkpoints staged locally
- [ ] Reference repo executed end-to-end in this workspace
- [ ] Metrics empirically reproduced in this workspace
- **Verdict:** BUILDABLE, with data and checkpoint staging still required

## 3. What We Take From The Paper

- The ForestSim dataset framing: 2094 photorealistic image/label pairs across 25 environments.
- The benchmark focus on unstructured forest perception with pixel-accurate segmentation labels.
- The random 90/10 train/test protocol from §VI-B.
- The 13-model benchmark suite from Table I.
- The evaluation metrics: mIoU, pixel accuracy, and mean pixel accuracy.
- The emphasis on data processing quality, ontology consistency, and reproducibility as core deliverables.

## 4. What We Skip

- Rebuilding the Unreal Engine environments and AirSim collection pipeline for MVP delivery.
- Collecting new synthetic data before reproduction of the published benchmark.
- Solving the paper’s future-work items such as domain adaptation to real-world datasets.
- Treating the raw reference repo as production-ready ANIMA code.

## 5. What We Adapt

- Convert the reference repository’s MMSeg-style configs into ANIMA-friendly config and registry layers.
- Normalize naming drift (`KODAMA`, `vail_all`, `forestsim_all`, `forestsim`) into a consistent `VIS-FORESTSIM` namespace.
- Support both the paper ontology and the repo’s 24-class / 6-class practical variants.
- Keep the published benchmark training recipes intact while exposing inference, API, Docker, and ROS2 entry points.
- Make local Mac inference possible while leaving heavy training to remote CUDA machines.

## 6. Architecture

### Inputs
- RGB image tensor: `Tensor[batch, 3, 512, 512]`
- Raw segmentation PNG: `Tensor[batch, 512, 512, 3]`
- Optional checkpoint ID: `Literal["pspnet_r50", "deeplabv3_r50", ..., "mask2former_swin_l"]`

### Outputs
- Segmentation logits: `Tensor[batch, classes, 512, 512]`
- Class ID mask: `Tensor[batch, 512, 512]`
- Colorized overlay: `Tensor[batch, 512, 512, 3]`
- Evaluation summary row: `{"model": str, "mIoU": float, "aAcc": float, "mAcc": float}`

### Main subsystems
1. `data/`: relabeling, ontology reconciliation, split generation, manifest building.
2. `datasets/`: ANIMA dataset adapters for 24-class and grouped 6-class variants.
3. `models/`: benchmark family registry, config resolution, checkpoint metadata.
4. `infer/`: predictor, visualization overlays, CLI.
5. `eval/`: metrics, Table I reproduction, regression reports.
6. `api/` and `ros2/`: downstream consumption layers.

## 7. Implementation Phases

### Phase 1 — Foundation + Reconciliation
- [ ] Fix module identity and package targets around `anima_vis_forestsim`
- [ ] Encode raw, 24-class, and 6-class ontologies
- [ ] Document paper-vs-repo mismatches and resolution rules
- [ ] Materialize benchmark config contracts

### Phase 2 — Reproduce Paper Benchmarks
- [ ] Build dataset conversion and split tooling
- [ ] Register the 13 paper benchmark families
- [ ] Run benchmark evaluation harness
- [ ] Recreate Table I comparison report

### Phase 3 — Productize Inference
- [ ] Package checkpoint registry and inference CLI
- [ ] Expose FastAPI and Docker surfaces
- [ ] Support ROS2 image-to-segmentation flow

### Phase 4 — Production Hardening
- [ ] Add artifact export, validation, and smoke tests
- [ ] Add graceful fallback for missing CUDA / missing checkpoints
- [ ] Publish benchmark and deployment reports

## 8. Datasets

| Dataset | Size | URL | Phase Needed |
|---------|------|-----|-------------|
| ForestSim raw RGB + segmentation | 2094 labeled pairs | https://vailforestsim.github.io/ | Phase 1 |
| ForestSim 24-class processed variant | derived | built locally from raw | Phase 1 |
| ForestSim grouped 6-class traversability variant | derived | built locally from raw | Phase 1 |

## 9. Dependencies on Other Wave Projects

| Needs output from | What it provides |
|------------------|------------------|
| None required for paper reproduction | — |
| Shared ANIMA ROS2 runtime conventions | topic naming and launch integration |
| Shared model artifact storage | checkpoint and report persistence |

## 10. Success Criteria

- Reproduce the 13 paper benchmark configurations in ANIMA config form.
- Recreate the paper split protocol and evaluation metrics.
- Match paper Table I mIoU within a reasonable tolerance on staged data and checkpoints.
- Produce an inference path for at least one high-performing published model.
- Expose that inference path through CLI, FastAPI, Docker, and ROS2 interfaces.

## 11. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| paper says 20 classes while repo exposes 24 and 6 | benchmark ambiguity | make ontology selection explicit and test both |
| repo config class counts (`150`, `171`) do not match dataset classes | silent training/eval failure | patch and validate head sizes in PRD-01 |
| dataset archive path is not yet staged locally | blocks reproduction | treat dataset staging as first milestone |
| reference repo is not ANIMA-native and may contain stale naming | maintenance drag | wrap, do not mirror, reference configs |
| 16-GPU paper training setup is not always available | slows exact reproduction | prioritize evaluation parity and single-checkpoint inference first |

## 12. Build Plan

| PRD# | Task | Outcome | Status |
|------|------|---------|--------|
| [PRD-01](prds/PRD-01-foundation.md) | Foundation | package identity, ontology, config, asset contracts | ⬜ |
| [PRD-02](prds/PRD-02-core-model.md) | Core Benchmark Stack | benchmark family registry and training config fidelity | ⬜ |
| [PRD-03](prds/PRD-03-inference.md) | Inference | checkpoint loading, prediction, overlays, CLI | ⬜ |
| [PRD-04](prds/PRD-04-evaluation.md) | Evaluation | split reproduction, metrics, Table I comparison | ⬜ |
| [PRD-05](prds/PRD-05-api-docker.md) | API + Docker | service contract and container packaging | ⬜ |
| [PRD-06](prds/PRD-06-ros2-integration.md) | ROS2 Integration | image subscriber and segmentation publisher | ⬜ |
| [PRD-07](prds/PRD-07-production.md) | Production | export, validation, artifact publication | ⬜ |

## 13. Immediate Next Step

Start with [PRD-01](prds/PRD-01-foundation.md). The first code session must resolve ontology and config drift before any benchmark run is trusted.
