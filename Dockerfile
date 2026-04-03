FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
COPY configs ./configs
COPY anima_module.yaml ./
RUN pip install --no-cache-dir uv
RUN uv sync --extra serve

CMD ["uv", "run", "uvicorn", "anima_vis_forestsim.serve:app", "--host", "0.0.0.0", "--port", "8000"]
