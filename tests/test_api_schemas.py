from anima_vis_forestsim.api.schemas import SegmentResponse


def test_schema_has_checkpoint_id() -> None:
    assert "checkpoint_id" in SegmentResponse.model_fields
