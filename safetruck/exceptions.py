# safetruck/exceptions.py
class TelemetryAnomalyError(ValueError):
    """Raised when incoming CAN bus frames contain structurally corrupted telemetry data."""
    pass

class SensorHardwareFault(OSError):
    """Raised when hardware registers encounter physical transmission dropouts."""
    pass
