"""Typed project settings for VIS-FORESTSIM."""

from __future__ import annotations

from pathlib import Path
import tomllib

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .data.manifest import AssetManifest, build_default_manifest
from .data.ontology import OntologySpec, resolve_ontology

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ForestSimSettings(BaseSettings):
    """Flat settings model with TOML + env override support."""

    model_config = SettingsConfigDict(
        env_prefix="ANIMA_VIS_FORESTSIM_",
        extra="ignore",
    )

    project_name: str = "anima-vis-forestsim"
    codename: str = "VIS-FORESTSIM"
    functional_name: str = "VIS-forestsim"
    wave: int = 7
    paper_arxiv: str = "2603.27923"
    python_version: str = "3.11"

    backend: str = "auto"
    precision: str = "fp32"
    default_ontology: str = "forestsim24"

    shared_volume: Path = Field(default=Path("/Volumes/AIFlowDev/RobotFlowLabs"))
    repos_volume: Path = Field(default=Path("/Volumes/AIFlowDev/RobotFlowLabs/repos/wave7"))
    server_data_root: Path = Field(default=Path("/mnt/forge-data"))
    server_artifacts_root: Path = Field(default=Path("/mnt/artifacts-datai"))

    zed2i: bool = True
    unitree_l2_lidar: bool = True
    cobot_xarm6: bool = False

    cuda_dependencies_enabled: bool = True
    mlx_dependencies_enabled: bool = True

    @property
    def is_server(self) -> bool:
        return self.server_data_root.exists()

    @property
    def dataset_root(self) -> Path:
        if self.is_server:
            return self.server_data_root / "datasets"
        return self.shared_volume / "datasets"

    @property
    def checkpoint_root(self) -> Path:
        if self.is_server:
            return self.server_data_root / "models"
        return self.shared_volume / "models"

    @property
    def artifacts_root(self) -> Path:
        if self.is_server:
            return self.server_artifacts_root
        return self.shared_volume / "artifacts"

    @property
    def ontology(self) -> OntologySpec:
        return resolve_ontology(self.default_ontology)

    @property
    def manifest(self) -> AssetManifest:
        return build_default_manifest(self.dataset_root, self.checkpoint_root)

    @classmethod
    def from_toml(cls, path: str | Path = "configs/default.toml") -> "ForestSimSettings":
        """Load settings from the project TOML file."""

        config_path = Path(path)
        if not config_path.is_absolute():
            repo_path = PROJECT_ROOT / config_path
            if repo_path.exists():
                config_path = repo_path
        with config_path.open("rb") as handle:
            raw = tomllib.load(handle)

        flattened = {
            "project_name": raw["project"]["name"],
            "codename": raw["project"]["codename"],
            "functional_name": raw["project"]["functional_name"],
            "wave": raw["project"]["wave"],
            "paper_arxiv": raw["project"]["paper_arxiv"],
            "python_version": raw["project"]["python_version"],
            "backend": raw["compute"]["backend"],
            "precision": raw["compute"]["precision"],
            "default_ontology": raw["compute"]["default_ontology"],
            "shared_volume": raw["data"]["shared_volume"],
            "repos_volume": raw["data"]["repos_volume"],
            "server_data_root": raw["data"]["server_data_root"],
            "server_artifacts_root": raw["data"]["server_artifacts_root"],
            "zed2i": raw["hardware"]["zed2i"],
            "unitree_l2_lidar": raw["hardware"]["unitree_l2_lidar"],
            "cobot_xarm6": raw["hardware"]["cobot_xarm6"],
            "cuda_dependencies_enabled": raw["dependencies"]["cuda_enabled"],
            "mlx_dependencies_enabled": raw["dependencies"]["mlx_enabled"],
        }
        return cls(**flattened)


def load_settings(path: str | Path = "configs/default.toml") -> ForestSimSettings:
    """Convenience loader for the default project settings."""

    return ForestSimSettings.from_toml(path)
