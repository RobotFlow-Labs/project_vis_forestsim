from anima_vis_forestsim.eval.report import render_table_i_report


def test_report_mentions_model_id() -> None:
    observed = {"m12": {"mIoU": 70.0, "aAcc": 92.0, "mAcc": 79.5}}
    report = render_table_i_report(observed=observed, expected={"m12": {"mIoU": 70.46, "aAcc": 92.14, "mAcc": 79.79}})
    assert "m12" in report
