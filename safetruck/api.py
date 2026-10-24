# safetruck/api.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
from safetruck.pipeline import ClosedLoopInferencePipeline

app = FastAPI(
    title="SafeTruck Privacy-First DDD API",
    description="AIS-198 Certified Camera-less Embedded Drowsiness Tracking Microservice"
)
pipeline = ClosedLoopInferencePipeline()

class TelemetryPayload(BaseModel):
    current_angle: float = Field(..., description="Latest raw steering angle reading from CAN bus", example=4.5)
    angle_window: List[float] = Field(..., min_items=5, description="30s historic sliding angle lookback array")
    speed_window: List[float] = Field(..., min_items=5, description="30s historic sliding vehicle velocity vector")

class PredictionResponse(BaseModel):
    sleep_level: int = Field(..., ge=0, le=3, description="Deduced cognitive degradation category integer [0-3]")
    status_msg: str = Field(..., description="Actionable HMI notification control phrase")

@app.post(
    "/api/v1/inference", 
    response_model=PredictionResponse, 
    status_code=status.HTTP_200_OK,
    summary="Compute Drowsiness Level Inference"
)
async def perform_inference(payload: TelemetryPayload):
    if not payload.speed_window:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Speed window array cannot be evaluated empty."
        )
        
    inferred_level = pipeline.run_tick(
        raw_angle=payload.current_angle,
        speed_history=payload.speed_window,
        angle_history=payload.angle_window
    )
    
    matrix_map = {
        0: "SYSTEM_SILENT",
        1: "ACTIVATE_CLUSTER_COFFEE_ICON",
        2: "ACTIVATE_CHIME_AND_STEERING_HAPTIC_MOTOR",
        3: "ACTIVATE_LOUD_ALARM_AND_PING_FLEET_CLOUD"
    }
    
    return PredictionResponse(
        sleep_level=inferred_level,
        status_msg=matrix_map.get(inferred_level, "SYSTEM_SILENT")
    )
