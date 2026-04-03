import numpy as np

from anima_vis_forestsim.data.ontology import FORESTSIM24
from anima_vis_forestsim.infer.overlay import colorize


def test_colorize_returns_rgb() -> None:
    mask = np.array([[0, 1], [2, 3]], dtype=np.uint8)
    assert colorize(mask, FORESTSIM24.palette).shape[-1] == 3
