"""CLI for local segmentation smoke tests and artifact generation."""

from __future__ import annotations

from pathlib import Path
import json

import cv2
import typer

from .predictor import ForestSimPredictor

app = typer.Typer(add_completion=False, help="VIS-FORESTSIM inference utilities.")


@app.command()
def run(
    image_path: Path,
    checkpoint_id: str = "m12",
    ontology: str = "forestsim24",
    output_dir: Path = Path("outputs/vis_forestsim"),
) -> None:
    """Run a local prediction pass and emit PNG + JSON outputs."""

    image_bgr = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise typer.BadParameter(f"Could not read image at {image_path}")

    predictor = ForestSimPredictor()
    result = predictor.predict(
        image_rgb=cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB),
        checkpoint_id=checkpoint_id,
        ontology=ontology,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    mask_path = output_dir / f"{image_path.stem}_{checkpoint_id}_mask.png"
    overlay_path = output_dir / f"{image_path.stem}_{checkpoint_id}_overlay.png"
    metadata_path = output_dir / f"{image_path.stem}_{checkpoint_id}_metadata.json"

    cv2.imwrite(str(mask_path), result.mask)
    cv2.imwrite(str(overlay_path), cv2.cvtColor(result.overlay, cv2.COLOR_RGB2BGR))
    metadata_path.write_text(
        json.dumps(
            {
                "checkpoint_id": result.checkpoint_id,
                "ontology": result.ontology,
                "used_stub": result.used_stub,
                "checkpoint_exists": result.checkpoint_exists,
                "warning": result.warning,
                "mask_path": str(mask_path),
                "overlay_path": str(overlay_path),
            },
            indent=2,
        )
    )

    typer.echo(f"mask={mask_path}")
    typer.echo(f"overlay={overlay_path}")
    typer.echo(f"metadata={metadata_path}")


if __name__ == "__main__":
    app()
