from pathlib import Path

from anima_vis_forestsim.data.manifest import build_default_manifest


def test_manifest_serializes() -> None:
    manifest = build_default_manifest(Path("/tmp/datasets"), Path("/tmp/models"))
    payload = manifest.to_dict()
    assert len(payload["datasets"]) == 3
    assert len(payload["reconciliation_findings"]) == 4
    assert payload["datasets"][0]["name"] == "forestsim_raw"
