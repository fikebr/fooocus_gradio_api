# Fooocus Gradio API Automation (Python)

Automate [Fooocus] via its Gradio API using a small, typed Python client and a simple CLI. This project lets you configure a generation in one call and trigger it in a second call, mirroring how Fooocus works under the hood.

> Works against a running Fooocus UI instance (local or remote). Images are saved by Fooocus itself in its usual output folder; this tool orchestrates the calls and provides logging and convenient defaults.

---

## Features

- Full generation configuration + trigger using the Gradio API
- Simple mode for quick text-to-image runs
- Endpoint inspector to help discover `fn_index` values
- Typed models with Pydantic for safer params
- Config via `.env` with sensible defaults
- Console + rotating file logging
- Ready for `uv` workflows (venv, install, run, test)

---

## Requirements

- Python 3.12+
- A running Fooocus instance (default URL `http://127.0.0.1:7865/`)
- `uv` package manager (recommended)

> If you do not have `uv`, install it (e.g., `pipx install uv` or `pip install uv`). See the official docs: `https://github.com/astral-sh/uv`.

---

## Quick start

1) Create a virtual environment

```bash
uv venv
```

2) Install dependencies from `pyproject.toml`

```bash
uv sync
```

3) Ensure Fooocus is running and reachable at `FOOOCUS_URL` (defaults to `http://127.0.0.1:7865/`).

4) Run a simple generation

```bash
uv run main.py --simple --prompt "a cozy cabin in the woods, cinematic lighting"
```

---

## Configuration

Configuration is loaded from environment variables (optionally via a `.env` file at the project root):

- `FOOOCUS_URL` (default: `http://127.0.0.1:7865/`) — base URL of Fooocus UI
- `LOG_FILE` (default: `logs/app.log`) — where rotating logs are written
- `REQUEST_TIMEOUT_SECONDS` (default: `300`) — request timeout for API operations

Example `.env`:

```env
FOOOCUS_URL=http://127.0.0.1:7865/
LOG_FILE=logs/app.log
REQUEST_TIMEOUT_SECONDS=300
```

---

## CLI usage

The CLI is implemented in `main.py` and supports both a simple route and a full configuration route.

- Inspect available endpoints (you must still pass `--prompt`, it will be ignored):

```bash
uv run main.py --inspect --prompt "placeholder"
```

- Simple generation:

```bash
uv run main.py \
  --simple \
  --prompt "a watercolor painting of a mountain village"
```

- Full configuration generation:

```bash
uv run main.py \
  --prompt "a futuristic city at night, neon lights, rain" \
  --negative_prompt "blurry, low quality" \
  --num_images 2 \
  --seed 42
```

Notes:
- The CLI prints a minimal result to stdout for scripting. Images are saved by Fooocus.
- `--seed` is a string; use `0` or `-1` for random behavior depending on your Fooocus build.

---

## Python API

Use the `FooocusClient` directly for programmatic control.

```python
from src.fooocus_client import FooocusClient
from src.models import GenerationParams

client = FooocusClient()  # uses FOOOCUS_URL from .env by default

# Quick run with defaults
result = client.generate_simple(prompt="a serene lakeside at sunset", num_images=1)
print(result)

# Full configuration
params = GenerationParams(
    prompt="a dragon flying over a medieval castle",
    negative_prompt="blurry, distorted",
    num_images=2,
    seed="0",
)
result = client.configure_and_generate(params)
print(result)
```

Key model fields (see `src/models.py`):
- `prompt`, `negative_prompt`, `num_images`, `seed`
- `styles`, `performance`, `aspect_ratio`, `output_format`
- `image_sharpness`, `guidance_scale`, `base_model`

> Internally, Fooocus often requires two calls: one to configure (large parameter list; commonly `fn_index=67`) and one to trigger (commonly `fn_index=68`). These indices can vary across Fooocus builds. Use the inspector below to discover current values.

---

## Discovering endpoints

```python
from src.fooocus_client import FooocusClient

client = FooocusClient()
info = client.inspect_endpoints()
print(info["summary"])  # shows counts and a short list of endpoints
```

Or via CLI:

```bash
uv run main.py --inspect --prompt "placeholder"
```

---

## Logging

Logging is configured for both console and file output (rotating) via `src/logger.py`. By default logs go to `logs/app.log`. You can customize the path using `LOG_FILE` in your `.env`.

---

## Project structure

```text
.
├─ docs/
│  ├─ automating_fooocus_chat.md
│  └─ notes.md
├─ src/
│  ├─ config.py            # loads .env into a typed AppConfig
│  ├─ fooocus_client.py    # FooocusClient adapter over gradio_client
│  ├─ logger.py            # console + rotating file logging
│  └─ models.py            # pydantic models (GenerationParams)
├─ main.py                 # CLI entrypoint
├─ pyproject.toml          # dependencies and metadata
├─ uv.lock                 # lockfile (managed by uv)
└─ README.md
```

---

## Development

- Install deps: `uv sync`
- Run the app: `uv run main.py --simple --prompt "..."`
- Run tests (pytest):

```bash
uv run -m pytest -q
```

---

## Troubleshooting

- Connection refused / timeouts: ensure Fooocus is running and `FOOOCUS_URL` is correct.
- Trigger deserialization error: some Fooocus builds return non-standard results from the trigger call; images are likely still saved. The client returns a soft-success with `status: triggered` in this case.
- `fn_index` changes across versions: use `--inspect` or `FooocusClient.inspect_endpoints()` to discover the current indices.
- Logs not written: ensure the `logs/` directory is writable or change `LOG_FILE`.

---

## Dependencies

Declared in `pyproject.toml`:
- `gradio-client`
- `pydantic`
- `python-dotenv`
- `fastapi` (reserved for potential future HTTP wrapper)
- `pickledb`
- `toml`
- `websockets`

---

## Acknowledgements

- Fooocus community and maintainers
- Gradio team for `gradio_client`

[Fooocus]: `https://github.com/lllyasviel/Fooocus`
