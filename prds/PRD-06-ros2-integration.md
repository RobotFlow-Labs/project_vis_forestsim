# PRD-06: ROS2 Integration

> Module: VIS-FORESTSIM | Priority: P2  
> Depends on: PRD-03, PRD-05  
> Status: ⬜ Not started

## Objective

Wrap the inference predictor in a ROS2 node that subscribes to camera images and publishes segmentation masks and overlays for downstream autonomy stacks.

## Context (from paper)

ForestSim targets intelligent vehicles operating in off-road environments. In ANIMA that means the benchmark model must eventually interoperate with ROS2 image streams and navigation modules.

**Paper reference**: motivation from Abstract, §III

## Acceptance Criteria

- [ ] ROS2 node subscribes to `sensor_msgs/msg/Image`.
- [ ] Node publishes raw mask, color overlay, and metadata topics.
- [ ] Parameters allow checkpoint selection and ontology selection.
- [ ] Launch file starts a minimal demo graph.
- [ ] Test: `uv run pytest tests/test_ros2_node.py -v` passes.

## Files to Create

| File | Purpose | Paper Ref | Est. Lines |
|------|---------|-----------|-----------|
| `src/anima_vis_forestsim/ros2/node.py` | ROS2 segmentation node | Abstract, §III | ~190 |
| `src/anima_vis_forestsim/ros2/launch/forestsim.launch.py` | launch entry | — | ~50 |
| `tests/test_ros2_node.py` | topic contract tests | — | ~80 |

## Architecture Detail (from paper)

### Inputs

`/camera/rgb/image_raw: sensor_msgs/msg/Image`

### Outputs

`/forestsim/mask: sensor_msgs/msg/Image`  
`/forestsim/overlay: sensor_msgs/msg/Image`  
`/forestsim/meta: std_msgs/msg/String`

### Algorithm

```python
# Derived from the paper's intelligent vehicle perception use case
class ForestSimNode(Node):
    def image_callback(self, msg):
        rgb = ros_image_to_numpy(msg)
        _, mask, overlay = predictor.predict(rgb, self.checkpoint_id, self.ontology)
        self.mask_pub.publish(numpy_to_ros_image(mask))
        self.overlay_pub.publish(numpy_to_ros_image(overlay))
```

## Dependencies

```toml
rclpy = "*"
cv-bridge = "*"
sensor-msgs = "*"
```

## Data Requirements

| Asset | Size | Path | Download |
|------|------|------|----------|
| serving checkpoint | variable | configurable ROS2 parameter | staged locally |

## Test Plan

```bash
uv run pytest tests/test_ros2_node.py -v
```

## References

- Paper: Abstract
- Paper: §III “Relevant Uses in Autonomy”
- Depends on: PRD-03, PRD-05
- Feeds into: PRD-07
