# safetruck/data_processing.py
import math
from typing import List, Tuple
from safetruck.config import logger, REVERSAL_THRESHOLD_DEG
from safetruck.exceptions import TelemetryAnomalyError

class KalmanFilterComponent:
    """Applies pure deterministic signal smoothing to raw CAN steering angle signals."""
    def __init__(self, alpha: float = 0.2):
        self._alpha = alpha
        self._prev_angle = 0.0

    def smooth(self, raw_angle: float) -> float:
        if math.isnan(raw_angle):
            logger.error("Received NaN value inside raw steering angle sequence.")
            raise TelemetryAnomalyError("Steering angle cannot be NaN.")
        
        smoothed = (self._alpha * raw_angle) + ((1.0 - self._alpha) * self._prev_angle)
        self._prev_angle = smoothed
        return smoothed

class FeatureEngine:
    """Extracts Steering Wheel Reversal Rates (SWRR) and speed standard deviation indicators."""
    @staticmethod
    def compute_swrr(angles: List[float]) -> int:
        if not angles:
            return 0
        reversals = 0
        for i in range(1, len(angles)):
            if abs(angles[i] - angles[i-1]) > REVERSAL_THRESHOLD_DEG:
                reversals += 1
        return reversals

    @staticmethod
    def compute_speed_std(speeds: List[float]) -> float:
        if not speeds:
            return 0.0
        mean_speed = sum(speeds) / len(speeds)
        variance = sum((x - mean_speed) ** 2 for x in speeds) / len(speeds)
        return math.sqrt(variance)
