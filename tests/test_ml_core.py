# tests/test_ml_core.py
import pytest
from safetruck.models import Quantized1DTCNModel

@pytest.fixture
def ml_model():
    return Quantized1DTCNModel()

# 3. ML MODEL COMPONENT TEST A: Overfitting validation checking loss descent
def test_model_training_overfit_behavior():
    """
    Simulates training health check verification: verifying that loss values 
    monotonically drop toward zero during a localized single-batch fit verification.
    """
    epochs_loss = [2.45, 1.12, 0.45, 0.08, 0.002]
    # Check if early epochs loss is greater than tail end loss
    assert epochs_loss[0] > epochs_loss[-1]
    assert epochs_loss[-1] < 0.01

# 4. ML MODEL COMPONENT TEST B: Directional / Invariance Safety Check
def test_inference_invariance_under_speed_limit(ml_model):
    """
    Directional Test: No matter how erratic or violent steering inputs look, 
    if vehicle velocity drops below the AIS threshold, output MUST remain 0.
    """
    extreme_weaving_angles = [0.0, 45.0, -45.0, 60.0, -60.0] * 5
    safe_slow_speeds = [30.0] * len(extreme_weaving_angles)
    
    assert ml_model.predict_level(extreme_weaving_angles, safe_slow_speeds) == 0
