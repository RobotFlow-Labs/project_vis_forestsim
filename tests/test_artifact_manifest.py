from anima_vis_forestsim.export import build_artifact_manifest


def test_manifest_contains_module_name() -> None:
    manifest = build_artifact_manifest("missing.pth", model_id="m12", ontology="forestsim24")
    assert manifest["module"] == "VIS-FORESTSIM"
