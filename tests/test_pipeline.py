# tests/test_pipeline.py
import pytest
import math
from safetruck.pipeline import ClosedLoopInferencePipeline
from safetruck.data_processing import KalmanFilterComponent
from safetruck.exceptions import TelemetryAnomalyError

@pytest.fixture
def active_pipeline():
    return ClosedLoopInferencePipeline()

# 1. UNIT TEST: Data Validation / Preprocessing Check
def test_kalman_filter_cleansing():
    filter_step = KalmanFilterComponent(alpha=0.5)
    first_pass = filter_step.smooth(10.0)
    assert first_pass == 5.0  # 0.5 * 10 + 0.5 * 0
    
    with pytest.raises(TelemetryAnomalyError):
        filter_step.smooth(math.nan)

# 2. INTEGRATION TEST: Verifying Inter-Component State Execution Flow
def test_pipeline_high_speed_weaving_integration(active_pipeline):
    mock_angles = [0.0, 5.0, -5.0, 5.0, -5.0, 6.0, -6.0, 7.0] * 3
    mock_speeds = [75.0] * len(mock_angles)
    
    result = active_pipeline.run_tick(
        raw_angle=8.0, 
        speed_history=mock_speeds, 
        angle_history=mock_angles
    )
    # High frequency micro-reversals above 65km/h must flag severe alerts
    assert result in [2, 3]
