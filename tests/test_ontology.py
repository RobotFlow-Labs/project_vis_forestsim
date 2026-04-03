from anima_vis_forestsim.data.ontology import FORESTSIM6, FORESTSIM24, resolve_ontology


def test_vail_all_alias_resolves_to_forestsim24() -> None:
    assert resolve_ontology("vail_all").name == "forestsim24"
    assert resolve_ontology("forestsim_all").num_classes == 24


def test_forestsim_alias_resolves_to_group6() -> None:
    assert resolve_ontology("forestsim").name == "forestsim6"
    assert resolve_ontology("forestsim_group6").num_classes == 6


def test_ontology_metadata_is_preserved() -> None:
    assert FORESTSIM24.paper_reference_count == 20
    assert FORESTSIM6.num_classes == 6
