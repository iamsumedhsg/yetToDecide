from typing import List, Optional
from pydantic import BaseModel, Field

class EventBase(BaseModel):
    event_id: str
    latitude: float
    longitude: float
    acq_date: str
    acq_time: str
    satellite: str = "VIIRS_SNPP"
    frp: float
    brightness_temperature: float
    confidence: str
    daynight: str

class EventMLContext(BaseModel):
    classification: str = Field(..., description="INDUSTRIAL or NATURAL")
    prediction_probability: float = Field(..., ge=0.0, le=1.0)
    model_version: str = "xgboost_v1_prototype"
    reasons: List[str] = []

class EventSpatialContext(BaseModel):
    nearest_industrial_facility: Optional[str] = None
    industrial_distance_km: float
    industrial_nearby: bool

class EventTemporalContext(BaseModel):
    hotspot_count_7d: int
    hotspot_count_30d: int
    hotspot_count_90d: int

class ThermalEvent(EventBase):
    classification: str
    prediction_probability: float
    model_version: str = "v1_prototype"
    nearest_industrial_facility: Optional[str] = None
    industrial_distance_km: float
    industrial_nearby: bool
    hotspot_count_7d: int
    hotspot_count_30d: int
    hotspot_count_90d: int
    land_cover: Optional[str] = "Built-up"
    reasons: List[str] = []

class GeoJSONGeometry(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]

class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: GeoJSONGeometry
    properties: ThermalEvent

class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]

class DashboardStats(BaseModel):
    total_events: int
    industrial_count: int
    natural_count: int
    avg_frp: float
    max_frp: float
    high_confidence_ratio: float
