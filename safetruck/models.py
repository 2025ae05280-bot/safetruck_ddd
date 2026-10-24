# safetruck/models.py
from typing import List
from safetruck.config import logger, AIS_MIN_SPEED_KMH
from safetruck.data_processing import FeatureEngine

class Quantized1DTCNModel:
    """Simulates production execution loop behavior of our INT8 compiled NPU model graph."""
    def predict_level(self, angles: List[float], speeds: List[float]) -> int:
        if not speeds or speeds[-1] < AIS_MIN_SPEED_KMH:
            logger.warning(f"Speed under operational limit ({speeds[-1] if speeds else 0} km/h). Alerts suppressed.")
            return 0
        
        reversals = FeatureEngine.compute_swrr(angles)
        speed_std = FeatureEngine.compute_speed_std(speeds)
        
        logger.info(f"ML Processing Telemetry: Reversals={reversals}, SpeedStd={speed_std:.2f}")
        
        if reversals > 15 and speed_std < 1.5:
            return 3  # Level 3: Micro-sleep
        elif reversals > 10:
            return 2  # Level 2: Severe Drowsiness
        elif reversals > 5:
            return 1  # Level 1: Mild Fatigue
        return 0      # Level 0: Active Alert
