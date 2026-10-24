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
