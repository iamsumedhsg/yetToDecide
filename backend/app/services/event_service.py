import json
from pathlib import Path
from typing import List, Optional
from ..schemas.event import (
    ThermalEvent,
    GeoJSONFeatureCollection,
    GeoJSONFeature,
    GeoJSONGeometry,
    DashboardStats
)

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "sample_events.json"

class EventService:
    def __init__(self, data_file: Path = DATA_PATH):
        self.data_file = data_file
        self._events: List[ThermalEvent] = []
        self._load_data()

    def _load_data(self):
        if self.data_file.exists():
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                self._events = [ThermalEvent(**item) for item in raw_data]
        else:
            self._events = []

    def get_events(
        self,
        classification: Optional[str] = None,
        min_frp: Optional[float] = None,
        min_confidence: Optional[float] = None,
        limit: Optional[int] = None
    ) -> List[ThermalEvent]:
        results = self._events
        if classification:
            results = [e for e in results if e.classification.upper() == classification.upper()]
        if min_frp is not None:
            results = [e for e in results if e.frp >= min_frp]
        if min_confidence is not None:
            results = [e for e in results if e.prediction_probability >= min_confidence]
        if limit:
            results = results[:limit]
        return results

    def get_event_by_id(self, event_id: str) -> Optional[ThermalEvent]:
        for e in self._events:
            if e.event_id == event_id:
                return e
        return None

    def get_geojson(
        self,
        classification: Optional[str] = None
    ) -> GeoJSONFeatureCollection:
        events = self.get_events(classification=classification)
        features = [
            GeoJSONFeature(
                geometry=GeoJSONGeometry(coordinates=[e.longitude, e.latitude]),
                properties=e
            )
            for e in events
        ]
        return GeoJSONFeatureCollection(features=features)

    def get_stats(self) -> DashboardStats:
        if not self._events:
            return DashboardStats(
                total_events=0,
                industrial_count=0,
                natural_count=0,
                avg_frp=0.0,
                max_frp=0.0,
                high_confidence_ratio=0.0
            )

        total = len(self._events)
        industrial = sum(1 for e in self._events if e.classification == "INDUSTRIAL")
        natural = sum(1 for e in self._events if e.classification == "NATURAL")
        frps = [e.frp for e in self._events]
        avg_frp = round(sum(frps) / total, 2)
        max_frp = round(max(frps), 2)
        high_conf = sum(1 for e in self._events if e.prediction_probability >= 0.90)

        return DashboardStats(
            total_events=total,
            industrial_count=industrial,
            natural_count=natural,
            avg_frp=avg_frp,
            max_frp=max_frp,
            high_confidence_ratio=round(high_conf / total, 2)
        )

event_service = EventService()
