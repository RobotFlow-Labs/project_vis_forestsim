# VIS-FORESTSIM — Asset Manifest

## Paper
- Title: ForestSim: A Synthetic Benchmark for Intelligent Vehicle Perception in Unstructured Forest Environments
- Alias in project docs: ForestSim: Off-Road Segmentation Benchmark
- ArXiv: 2603.27923
- Authors: Pragat Wagle, Zheng Chen, Lantao Liu
- Dataset site: https://vailforestsim.github.io/
- Reference repo: https://github.com/pragatwagle/ForestSim

## Status: ALMOST

Paper and reference repository are present locally. Dataset archives and pretrained checkpoints are still remote assets and must be staged before reproduction.

## Pretrained Weights
| Model | Purpose | Source | Target Path | Status |
|-------|---------|--------|-------------|--------|
| `torchvision://resnet50` | PSPNet, DeepLabV3, DeepLabV3+ backbones, Mask2Former-R50 | TorchVision builtin | `/mnt/forge-data/models/vision/torchvision/resnet50/` | REMOTE |
| `torchvision://resnet101` | Mask2Former-R101 backbone | TorchVision builtin | `/mnt/forge-data/models/vision/torchvision/resnet101/` | REMOTE |
| `open-mmlab://resnet101_v1c` | DeepLabV3-R101, DeepLabV3+-R101 backbone | OpenMMLab builtin alias | `/mnt/forge-data/models/vision/openmmlab/resnet101_v1c/` | REMOTE |
| `https://download.openmmlab.com/mmsegmentation/v0.5/pretrain/segformer/mit_b0_20220624-7e0fe6dd.pth` | SegFormer-B0 backbone | OpenMMLab | `/mnt/forge-data/models/vision/openmmlab/segformer/mit_b0_20220624-7e0fe6dd.pth` | REMOTE |
| `https://download.openmmlab.com/mmsegmentation/v0.5/pretrain/segformer/mit_b5_20220624-658746d9.pth` | SegFormer-B5 backbone | OpenMMLab | `/mnt/forge-data/models/vision/openmmlab/segformer/mit_b5_20220624-658746d9.pth` | REMOTE |
| `https://download.openmmlab.com/mmsegmentation/v0.5/pretrain/swin/swin_tiny_patch4_window7_224_20220317-1cdeb081.pth` | Mask2Former-Swin-T backbone | OpenMMLab | `/mnt/forge-data/models/vision/openmmlab/swin/swin_tiny_patch4_window7_224_20220317-1cdeb081.pth` | REMOTE |
| `https://download.openmmlab.com/mmsegmentation/v0.5/pretrain/swin/swin_small_patch4_window7_224_20220317-7ba6d6dd.pth` | Mask2Former-Swin-S backbone | OpenMMLab | `/mnt/forge-data/models/vision/openmmlab/swin/swin_small_patch4_window7_224_20220317-7ba6d6dd.pth` | REMOTE |
| `https://download.openmmlab.com/mmsegmentation/v0.5/pretrain/swin/swin_base_patch4_window12_384_20220317-55b0104a.pth` | Mask2Former-Swin-B backbone | OpenMMLab | `/mnt/forge-data/models/vision/openmmlab/swin/swin_base_patch4_window12_384_20220317-55b0104a.pth` | REMOTE |
| `https://download.openmmlab.com/mmsegmentation/v0.5/pretrain/swin/swin_large_patch4_window12_384_22k_20220412-6580f57d.pth` | Mask2Former-Swin-L backbone | OpenMMLab | `/mnt/forge-data/models/vision/openmmlab/swin/swin_large_patch4_window12_384_22k_20220412-6580f57d.pth` | REMOTE |

## Datasets
| Dataset | Size | Split | Source | Target Path | Status |
|---------|------|-------|--------|-------------|--------|
| ForestSim raw RGB + segmentation | 2094 image/label pairs, 25 environments | paper reports random 90/10 train/test | https://vailforestsim.github.io/ | `/mnt/forge-data/datasets/vision/forestsim/raw/` | REMOTE |
| ForestSim processed 24-class MMSeg variant (`forestsim_all`) | 2094 pairs after relabeling | `train`, `test` | built from raw via repo converters | `/mnt/forge-data/datasets/vision/forestsim/forestsim_all/` | MISSING |
| ForestSim grouped 6-class traversability variant (`forestsim`) | derived from 24-class palette using `Groups` map | `train`, `val`, `test` in repo layout | built from raw via repo converters | `/mnt/forge-data/datasets/vision/forestsim/forestsim_group6/` | MISSING |

## Training Recipe
| Param | Value | Paper / Repo Reference |
|-------|-------|------------------------|
| input crop | `512x512` | repo configs `configs/_base_/datasets/*.py` |
| split strategy | random `90%` train / `10%` test | paper §VI-B |
| PSPNet / DeepLab / DeepLabV3+ optimizer | SGD, `lr=0.01`, `momentum=0.9`, `weight_decay=5e-4` | repo `configs/_base_/schedules/schedule_40k.py` |
| PSPNet / DeepLab / DeepLabV3+ iterations | `40,000` | repo `schedule_40k.py`, paper §VI-B |
| SegFormer optimizer | AdamW, `lr=6e-5`, `betas=(0.9, 0.999)`, `weight_decay=0.01` | repo `segformer_mit-b0_8xb2-160k_forestsim_all-512x512.py` |
| SegFormer scheduler | Linear warmup to PolyLR, warmup `1500` iters, end `160000` | repo `segformer_mit-b0_8xb2-160k_forestsim_all-512x512.py` |
| Mask2Former optimizer | AdamW, `lr=1e-4`, `weight_decay=0.05`, grad clip `0.01` | repo `mask2former_r50_8xb2-160k_forestsim_all-512x512.py` |
| Mask2Former iterations | `160,000`, `val_interval=5000` | repo `mask2former_r50_8xb2-160k_forestsim_all-512x512.py`, paper §VI-B |
| training hardware | 4 nodes, 4 NVIDIA A100 GPUs per node | paper §VI-B |

## Expected Metrics From Paper
| Model | mIoU | Pixel Accuracy | Mean Pixel Accuracy |
|-------|------|----------------|---------------------|
| PSPNet-R50 (`m1`) | `61.64` | `89.85` | `72.14` |
| DeepLabV3-R50 (`m2`) | `61.87` | `89.91` | `72.81` |
| DeepLabV3-R101 (`m3`) | `62.81` | `89.86` | `73.13` |
| DeepLabV3+-R50 (`m4`) | `59.16` | `89.31` | `72.93` |
| DeepLabV3+-R101 (`m5`) | `59.22` | `88.32` | `69.56` |
| SegFormer-B0 (`m6`) | `61.82` | `90.52` | `71.12` |
| SegFormer-B5 (`m7`) | `67.93` | `92.05` | `76.42` |
| Mask2Former-R50 (`m8`) | `67.48` | `91.34` | `75.77` |
| Mask2Former-R101 (`m9`) | `65.80` | `91.29` | `74.61` |
| Mask2Former-Swin-B (`m10`) | `74.50` | `92.57` | `82.30` |
| Mask2Former-Swin-L (`m11`) | `75.31` | `92.65` | `82.68` |
| Mask2Former-Swin-T (`m12`) | `70.46` | `92.14` | `79.79` |
| Mask2Former-Swin-S (`m13`) | `74.02` | `92.39` | `81.39` |

## Reconciliation Risks To Resolve In PRD-01
| Item | Paper | Repo | Required Action |
|------|-------|------|-----------------|
| class count | 20 classes | 24-class dataset class plus 6-class grouped variant | encode both ontologies and document which one backs each experiment |
| benchmark naming | ForestSim | many repo paths still use `vail_all` | normalize naming in ANIMA package while preserving compatibility aliases |
| head class counts | paper implies 20 or 24 practical classes | configs set `num_classes=150` or `171` in multiple files | explicitly patch head sizes before reproduction |
| split layout | train/test only in paper | group6 repo config expects train/val/test | define canonical ANIMA split contract and conversion rules |
