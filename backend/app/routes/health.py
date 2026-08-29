from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Health"])

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str

@router.get("/health", response_model=HealthResponse)
def get_health():
    return HealthResponse(
        status="ok",
        service="SIH Thermal Anomaly Backend",
        version="0.1.0"
    )
