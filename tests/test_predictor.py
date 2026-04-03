import numpy as np

from anima_vis_forestsim.infer.predictor import ForestSimPredictor


def test_predictor_returns_mask_shape() -> None:
    image = np.full((80, 120, 3), 128, dtype=np.uint8)
    result = ForestSimPredictor().predict(image, checkpoint_id="m12", ontology="forestsim24")
    assert result.mask.shape[-2:] == (512, 512)
    assert result.logits.shape[1] == 24
    assert result.used_stub is True
