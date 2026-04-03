# VIS-FORESTSIM

## Paper
**ForestSim: Off-Road Segmentation Benchmark**
arXiv: https://arxiv.org/abs/2603.27923

## Module Identity
- Codename: VIS-FORESTSIM
- Domain: Vision
- Part of ANIMA Intelligence Compiler Suite

## Structure
```
project_vis_forestsim/
├── pyproject.toml
├── configs/
├── src/anima_vis_forestsim/
├── tests/
├── scripts/
├── papers/          # Paper PDF
├── AGENTS.md        # This file
├── NEXT_STEPS.md
├── ASSETS.md
└── PRD.md
```

## Commands
```bash
uv sync
uv run pytest
uv run ruff check src/ tests/
uv run ruff format src/ tests/
```

## Conventions
- Package manager: uv (never pip)
- Build backend: hatchling
- Python: >=3.10
- Config: TOML + Pydantic BaseSettings
- Lint: ruff
- Git commit prefix: [VIS-FORESTSIM]
