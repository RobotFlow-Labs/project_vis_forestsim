from pathlib import Path

from anima_vis_forestsim.config import ForestSimSettings, load_settings


def test_settings_load_project_defaults() -> None:
    settings = load_settings()
    assert settings.project_name == "anima-vis-forestsim"
    assert settings.codename == "VIS-FORESTSIM"
    assert settings.python_version == "3.11"
    assert settings.default_ontology == "forestsim24"


def test_settings_accept_alias_paths() -> None:
    settings = ForestSimSettings(
        shared_volume=Path("/tmp/shared"),
        repos_volume=Path("/tmp/repos"),
        server_data_root=Path("/tmp/server"),
        server_artifacts_root=Path("/tmp/artifacts"),
    )
    assert settings.default_ontology == "forestsim24"
    assert settings.dataset_root == Path("/tmp/shared/datasets")
    assert settings.checkpoint_root == Path("/tmp/shared/models")
