# safetruck/config.py
import logging

AIS_MIN_SPEED_KMH = 65.0
BUFFER_SIZE = 1500  # 30 seconds at 50Hz
REVERSAL_THRESHOLD_DEG = 2.0

# Centralized Logger Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("SafeTruckDDD")
