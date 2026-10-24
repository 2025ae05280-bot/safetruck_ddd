safetruck_ddd/
│
├── safetruck/
│   ├── __init__.py
│   ├── config.py           # Hardcoded settings & AIS-198 compliance parameters
│   ├── exceptions.py       # Custom domain-specific telemetry exceptions
│   ├── data_processing.py  # Kalman filter, ring windowing, feature engines
│   ├── models.py           # 1D-TCN model simulation wrapper (INT8 behavior)
│   ├── pipeline.py         # End-to-end execution coordinator core
│   └── api.py              # FastAPI REST API wrapper implementation
│
└── tests/
    ├── __init__.py
    ├── test_pipeline.py    # Unit, integration, & data schema validation tests
    └── test_ml_core.py     # Overfitting test & inference directional checks
