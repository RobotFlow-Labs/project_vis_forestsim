from pathlib import Path

from anima_vis_forestsim.models.checkpoints import resolve_checkpoint, resolve_checkpoint_spec


def test_checkpoint_path_has_pth_suffix(tmp_path: Path) -> None:
    assert resolve_checkpoint("m12", tmp_path).suffix == ".pth"


def test_checkpoint_spec_reports_missing_file(tmp_path: Path) -> None:
    resolved = resolve_checkpoint_spec("m12", tmp_path)
    assert resolved.exists is False
