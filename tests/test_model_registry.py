from anima_vis_forestsim.models.registry import PAPER_TABLE, get_model_spec


def test_registry_contains_all_paper_models() -> None:
    assert len(PAPER_TABLE) == 13


def test_registry_exposes_best_model_targets() -> None:
    spec = get_model_spec("m11")
    assert spec.family == "mask2former"
    assert spec.paper_miou == 75.31
