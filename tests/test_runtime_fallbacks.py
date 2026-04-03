from pathlib import Path

from anima_vis_forestsim.config import ForestSimSettings
from anima_vis_forestsim.runtime_checks import validate_runtime


def test_missing_checkpoint_returns_warning(tmp_path: Path) -> None:
    settings = ForestSimSettings(
        shared_volume=tmp_path,
        server_data_root=tmp_path / "missing-server",
        server_artifacts_root=tmp_path / "artifacts",
    )
    warnings = validate_runtime(settings=settings, checkpoint_id="m12")
    assert any("Checkpoint not staged" in item for item in warnings)
