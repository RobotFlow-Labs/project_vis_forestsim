import numpy as np

from anima_vis_forestsim.infer.predictor import ForestSimPredictor
from anima_vis_forestsim.eval.runner import run_eval


def test_eval_runner_returns_summary() -> None:
    predictor = ForestSimPredictor()
    example_image = np.full((32, 32, 3), 100, dtype=np.uint8)
    target_mask = predictor.predict(example_image, checkpoint_id="m12", ontology="forestsim24").mask
    summary = run_eval(
        predictor,
        split=[{"image": example_image, "target_mask": target_mask}],
        checkpoint_id="m12",
        ontology="forestsim24",
    )
    assert "aAcc" in summary
    assert "mIoU" in summary
