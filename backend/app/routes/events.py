from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from ..schemas.event import ThermalEvent, GeoJSONFeatureCollection, DashboardStats
from ..services.event_service import event_service

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("", response_model=List[ThermalEvent])
def list_events(
    classification: Optional[str] = Query(None, description="Filter by classification: INDUSTRIAL or NATURAL"),
    min_frp: Optional[float] = Query(None, description="Minimum FRP threshold in MW"),
    min_confidence: Optional[float] = Query(None, description="Minimum AI probability threshold (0.0 to 1.0)"),
    limit: Optional[int] = Query(100, ge=1, le=1000, description="Max records to return")
):
    """
    Retrieve thermal anomaly events with optional classification and FRP filtering.
    """
    return event_service.get_events(
        classification=classification,
        min_frp=min_frp,
        min_confidence=min_confidence,
        limit=limit
    )

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats():
    """
    Get summary statistics for the dashboard.
    """
    return event_service.get_stats()

@router.get("/geojson", response_model=GeoJSONFeatureCollection)
def get_events_geojson(
    classification: Optional[str] = Query(None, description="Filter GeoJSON by classification")
):
    """
    Retrieve thermal anomaly events in GeoJSON format for direct GIS/Leaflet/Mapbox integration.
    """
    return event_service.get_geojson(classification=classification)

@router.get("/{event_id}", response_model=ThermalEvent)
def get_event_detail(event_id: str):
    """
    Retrieve detailed parameters and ML reasoning for a specific thermal anomaly event.
    """
    event = event_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
    return event
