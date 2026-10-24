safetruck_ddd/
│
├── safetruck/
│   ├── __init__.py
│   ├── config.py           # Hardcoded settings & AIS-198 compliance parameters
│   ├── exceptions.py       # Custom domain-specific telemetry exceptions
│   ├── data_processing.py  # Kalman filter, signal processing, feature engineering
│   ├── models.py           # Production-style inference model wrapper
│   ├── pipeline.py         # End-to-end inference coordinator
│   └── api.py              # FastAPI REST API wrapper implementation
│
├── tests/
│   ├── __init__.py
│   ├── test_pipeline.py    # Unit/integration validation
│   └── test_ml_core.py     # Overfitting and invariance checks
├── pytest.ini             # Ensures the project root is on PYTHONPATH during pytest runs
├── requirements.txt       # Runtime/test dependencies for the ML service stack
├── run_lint_pipeline.py   # Demonstrates research-vs-production refactoring workflow
└── README.md

SafeTruck DDD project overview:
- Refactored ML application logic into domain modules for configuration, telemetry
  processing, model inference, and pipeline orchestration.
- Added production-style error handling and logging in the critical execution path.
- Exposed deterministic inference through a FastAPI endpoint.
- Included QA coverage for unit/integration checks and model behavior invariance.

Setup:
  python3 -m pip install -r requirements.txt
  pytest -q

Run the API locally:
  uvicorn safetruck.api:app --reload

Open `http://127.0.0.1:8000/` for service information, or
`http://127.0.0.1:8000/docs` for the interactive API documentation. Submit
inference requests to `POST /api/v1/inference`.

### Inference examples

In `/docs`, expand `POST /api/v1/inference`, select **Try it out**, paste one
of the request bodies below, and select **Execute**. Each example shows the
expected response from a fresh pipeline.

#### Level 0 — active alert

Example 1 (speed below the 65 km/h operating threshold):

```json
{
  "current_angle": 0,
  "angle_window": [0, 20, -20, 20, -20, 0],
  "speed_window": [40, 42, 38, 41, 39]
}
```

Example 2 (steady steering at operating speed):

```json
{
  "current_angle": 0,
  "angle_window": [0, 0, 0, 0, 0, 0],
  "speed_window": [75, 75, 75, 75, 75]
}
```

Expected response for both:

```json
{
  "sleep_level": 0,
  "status_msg": "SYSTEM_SILENT"
}
```

#### Level 1 — mild fatigue

Example 1:

```json
{
  "current_angle": 0,
  "angle_window": [0, 4, 0, 4, 0, 4, 0, 4],
  "speed_window": [75, 75, 75, 75, 75]
}
```

Example 2:

```json
{
  "current_angle": 0,
  "angle_window": [0, 5, 0, 5, 0, 5, 0, 5],
  "speed_window": [80, 80, 80, 80, 80]
}
```

Expected response for both:

```json
{
  "sleep_level": 1,
  "status_msg": "ACTIVATE_CLUSTER_COFFEE_ICON"
}
```

#### Level 2 — severe drowsiness

Example 1:

```json
{
  "current_angle": 0,
  "angle_window": [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4],
  "speed_window": [75, 75, 75, 75, 75]
}
```

Example 2:

```json
{
  "current_angle": 0,
  "angle_window": [0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5],
  "speed_window": [80, 80, 80, 80, 80]
}
```

Expected response for both:

```json
{
  "sleep_level": 2,
  "status_msg": "ACTIVATE_CHIME_AND_STEERING_HAPTIC_MOTOR"
}
```

#### Level 3 — micro-sleep

Example 1:

```json
{
  "current_angle": 0,
  "angle_window": [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4],
  "speed_window": [75, 75, 75, 75, 75]
}
```

Example 2:

```json
{
  "current_angle": 0,
  "angle_window": [0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5],
  "speed_window": [80, 80, 80, 80, 80]
}
```

Expected response for both:

```json
{
  "sleep_level": 3,
  "status_msg": "ACTIVATE_LOUD_ALARM_AND_PING_FLEET_CLOUD"
}
```
