from anima_vis_forestsim.data.ontology import FORESTSIM24
from anima_vis_forestsim.models.config_emit import emit_config


def test_emitted_config_uses_ontology_class_count() -> None:
    cfg = emit_config("m12", FORESTSIM24)
    assert cfg["num_classes"] == 24


def test_emitted_config_preserves_paper_metrics() -> None:
    cfg = emit_config("m10", FORESTSIM24)
    assert cfg["paper_metrics"]["mIoU"] == 74.50
