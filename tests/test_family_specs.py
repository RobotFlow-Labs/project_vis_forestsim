from anima_vis_forestsim.models.families import FAMILY_SPECS


def test_mask2former_family_uses_160k_iters() -> None:
    assert FAMILY_SPECS["mask2former"].max_iters == 160000
