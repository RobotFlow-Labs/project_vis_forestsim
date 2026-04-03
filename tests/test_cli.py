from pathlib import Path

import cv2
import numpy as np
from typer.testing import CliRunner

from anima_vis_forestsim.infer.cli import app


def test_cli_help() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_cli_run_emits_outputs(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.png"
    image = np.full((32, 32, 3), 200, dtype=np.uint8)
    cv2.imwrite(str(image_path), image)

    runner = CliRunner()
    result = runner.invoke(app, [str(image_path), "--output-dir", str(tmp_path / "out")])

    assert result.exit_code == 0
    assert "metadata=" in result.stdout
