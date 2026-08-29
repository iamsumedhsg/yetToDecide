import math
from typing import List, Dict, Any, Tuple, Optional

# Reference industrial infrastructure dataset (India Key Facilities)
INDUSTRIAL_FACILITIES = [
    {"name": "Gujarat Refinery & Petrochemical Complex (Koyali, Vadodara)", "lat": 22.3072, "lon": 73.1812, "type": "Refinery/Petrochemical"},
    {"name": "Jamnagar Oil Refinery (RIL Complex)", "lat": 22.3524, "lon": 71.3255, "type": "Refinery"},
    {"name": "Angul Steel & Thermal Power Hub (Odisha)", "lat": 20.8880, "lon": 85.1511, "type": "Steel/Power"},
    {"name": "Korba Super Thermal Power Station (Chhattisgarh)", "lat": 22.3587, "lon": 82.6867, "type": "Thermal Power Plant"},
    {"name": "Mundra Thermal Power Project & Port (Gujarat)", "lat": 22.8251, "lon": 69.7042, "type": "Power/Industrial Port"},
    {"name": "Singrauli Coal Mining & Power Belt (MP/UP)", "lat": 24.2012, "lon": 82.6644, "type": "Coal Mining/Power"},
    {"name": "Visakhapatnam Steel & Petroleum Complex (AP)", "lat": 17.6322, "lon": 83.1678, "type": "Steel/Petroleum"},
    {"name": "Bhilai Steel Plant (Chhattisgarh)", "lat": 21.1938, "lon": 81.3805, "type": "Steel Plant"},
    {"name": "Manali Industrial & Petrochemical Area (Chennai)", "lat": 13.1684, "lon": 80.2642, "type": "Petrochemical/Industrial"},
    {"name": "Haldia Petrochemicals & Oil Terminal (West Bengal)", "lat": 22.0621, "lon": 88.0845, "type": "Petrochemical/Port"}
]

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the great-circle distance between two points on Earth in kilometers.
    """
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class OSMIndustrialService:
    """
    Spatial service to query distance to nearest industrial facility.
    """
    def __init__(self, facilities: List[Dict[str, Any]] = INDUSTRIAL_FACILITIES):
        self.facilities = facilities

    def find_nearest_facility(
        self,
        lat: float,
        lon: float,
        threshold_km: float = 2.0
    ) -> Tuple[Optional[str], float, bool]:
        """
        Finds the nearest industrial facility for a given latitude and longitude.
        Returns: (facility_name, distance_km, is_nearby_boolean)
        """
        if not self.facilities:
            return None, 999.0, False

        min_dist = float("inf")
        nearest_name = None

        for fac in self.facilities:
            dist = haversine_distance(lat, lon, fac["lat"], fac["lon"])
            if dist < min_dist:
                min_dist = dist
                nearest_name = fac["name"]

        min_dist = round(min_dist, 2)
        is_nearby = min_dist <= threshold_km

        return nearest_name, min_dist, is_nearby

osm_service = OSMIndustrialService()
