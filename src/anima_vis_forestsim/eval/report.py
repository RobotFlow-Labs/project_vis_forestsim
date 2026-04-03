"""Table I comparison reporting for reproduced benchmark rows."""

from __future__ import annotations

from typing import Any

from ..models.registry import PAPER_TABLE


def _expected_table(expected: dict[str, Any] | None = None) -> dict[str, dict[str, float]]:
    if expected is not None:
        return expected

    table: dict[str, dict[str, float]] = {}
    for model_id, spec in PAPER_TABLE.items():
        table[model_id] = {
            "mIoU": spec.paper_miou,
            "aAcc": spec.paper_aacc,
            "mAcc": spec.paper_macc,
        }
    return table


def render_table_i_report(
    observed: dict[str, dict[str, float]],
    expected: dict[str, dict[str, float]] | None = None,
) -> str:
    """Render a Markdown report comparing observed metrics with Table I targets."""

    expected_table = _expected_table(expected)
    lines = [
        "# ForestSim Table I Comparison",
        "",
        "| Model | Paper mIoU | Observed mIoU | Delta mIoU | Paper aAcc | Observed aAcc | Paper mAcc | Observed mAcc |",
        "|-------|------------|---------------|------------|------------|---------------|------------|---------------|",
    ]
    for model_id in sorted(expected_table):
        expected_row = expected_table[model_id]
        observed_row = observed.get(model_id, {})
        observed_miou = observed_row.get("mIoU")
        observed_aacc = observed_row.get("aAcc")
        observed_macc = observed_row.get("mAcc")
        delta = None if observed_miou is None else observed_miou - expected_row["mIoU"]
        lines.append(
            "| {model_id} | {paper_miou:.2f} | {observed_miou} | {delta} | {paper_aacc:.2f} | {observed_aacc} | {paper_macc:.2f} | {observed_macc} |".format(
                model_id=model_id,
                paper_miou=expected_row["mIoU"],
                observed_miou="-" if observed_miou is None else f"{observed_miou:.2f}",
                delta="-" if delta is None else f"{delta:+.2f}",
                paper_aacc=expected_row["aAcc"],
                observed_aacc="-" if observed_aacc is None else f"{observed_aacc:.2f}",
                paper_macc=expected_row["mAcc"],
                observed_macc="-" if observed_macc is None else f"{observed_macc:.2f}",
            )
        )
    return "\n".join(lines)
