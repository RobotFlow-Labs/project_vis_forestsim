from pathlib import Path

import cv2
import numpy as np
from fastapi.testclient import TestClient

from anima_vis_forestsim.api.app import app


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_segment_path_endpoint(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.png"
    image = np.full((16, 16, 3), 64, dtype=np.uint8)
    cv2.imwrite(str(image_path), image)

    client = TestClient(app)
    response = client.post(
        "/segment/path",
        json={"image_path": str(image_path), "checkpoint_id": "m12", "ontology": "forestsim24"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["checkpoint_id"] == "m12"
    assert body["mask_png_base64"]
