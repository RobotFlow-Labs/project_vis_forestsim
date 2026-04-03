import numpy as np

from anima_vis_forestsim.eval.metrics import build_confusion_matrix, per_class_iou, summarize_metrics


def test_metrics_include_miou() -> None:
    pred = np.array([[0, 1], [1, 0]], dtype=np.uint8)
    target = np.array([[0, 1], [0, 0]], dtype=np.uint8)
    confusion = build_confusion_matrix(pred, target, num_classes=2)
    summary = summarize_metrics(confusion)
    assert "mIoU" in summary


def test_sparse_class_nan_handling() -> None:
    confusion = np.array(
        [
            [10, 0, 0],
            [0, 5, 0],
            [0, 0, 0],
        ],
        dtype=np.int64,
    )
    iou = per_class_iou(confusion)
    assert np.isnan(iou[2])
