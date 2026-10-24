# safetruck/pipeline.py
from typing import List
from safetruck.config import logger
from safetruck.data_processing import KalmanFilterComponent
from safetruck.models import Quantized1DTCNModel
from safetruck.exceptions import TelemetryAnomalyError

class ClosedLoopInferencePipeline:
    """Manages secure sequence transitions, acting as the structural safety boundary firewall."""
    def __init__(self):
        self.filter = KalmanFilterComponent()
        self.model = Quantized1DTCNModel()

    def run_tick(self, raw_angle: float, speed_history: List[float], angle_history: List[float]) -> int:
        try:
            # 1. Deterministic Signal Cleansing
            smoothed_angle = self.filter.smooth(raw_angle)
            processed_angles = angle_history + [smoothed_angle]
            
            # 2. Sandboxed Machine Learning Prediction
            predicted_state = self.model.predict_level(processed_angles, speed_history)
            return predicted_state
            
        except TelemetryAnomalyError as tae:
            logger.error(f"[FIREWALL ACTION] Telemetry anomaly caught: {tae}. Safe fallback to Level 0.")
            return 0
        except Exception as e:
            logger.critical(f"[SYSTEM FAILURE] Unexpected runtime exception: {str(e)}. Defaulting to safe state.")
            return 0
