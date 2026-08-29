import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timedelta

# India Bounding Box limits (Approx: 6.5° N to 35.5° N, 68.0° E to 97.5° E)
INDIA_BBOX = {
    "min_lat": 6.5,
    "max_lat": 35.5,
    "min_lon": 68.0,
    "max_lon": 97.5
}

class FIRMSDataParser:
    """
    Parser for NASA FIRMS VIIRS Standard Processing (SP) CSV files.
    """
    def __init__(self, bbox: Dict[str, float] = INDIA_BBOX):
        self.bbox = bbox

    def load_firms_csv(self, file_path: Path) -> pd.DataFrame:
        """
        Loads and cleans raw NASA FIRMS CSV.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"FIRMS data file not found: {file_path}")

        df = pd.read_csv(file_path)
        
        # Standardize column names to lowercase
        df.columns = [col.lower() for col in df.columns]

        # Ensure required columns exist
        required_cols = {"latitude", "longitude", "acq_date", "acq_time", "frp", "confidence"}
        if not required_cols.issubset(set(df.columns)):
            missing = required_cols - set(df.columns)
            raise ValueError(f"Missing required FIRMS columns: {missing}")

        # Filter India bounding box
        df = df[
            (df["latitude"] >= self.bbox["min_lat"]) & (df["latitude"] <= self.bbox["max_lat"]) &
            (df["longitude"] >= self.bbox["min_lon"]) & (df["longitude"] <= self.bbox["max_lon"])
        ].copy()

        # Parse datetime
        df["acq_datetime"] = pd.to_datetime(
            df["acq_date"].astype(str) + " " + df["acq_time"].astype(str).str.zfill(4),
            format="%Y-%m-%d %H%M",
            errors="coerce"
        )

        return df

    def calculate_temporal_persistence(
        self,
        df: pd.DataFrame,
        radius_km: float = 1.0
    ) -> pd.DataFrame:
        """
        Calculates temporal persistence features (hotspot counts in 7d, 30d, 90d window within radius_km).
        """
        # Convert lat/lon distance approximation (1 deg ~ 111 km)
        delta_deg = radius_km / 111.0
        
        counts_7d, counts_30d, counts_90d = [], [], []

        for idx, row in df.iterrows():
            current_time = row["acq_datetime"]
            lat, lon = row["latitude"], row["longitude"]

            if pd.isna(current_time):
                counts_7d.append(1)
                counts_30d.append(1)
                counts_90d.append(1)
                continue

            # Filter nearby spatial events
            spatial_mask = (
                (df["latitude"].between(lat - delta_deg, lat + delta_deg)) &
                (df["longitude"].between(lon - delta_deg, lon + delta_deg))
            )
            nearby_df = df[spatial_mask]

            # Filter prior temporal windows
            t_7d = current_time - timedelta(days=7)
            t_30d = current_time - timedelta(days=30)
            t_90d = current_time - timedelta(days=90)

            c7 = len(nearby_df[(nearby_df["acq_datetime"] >= t_7d) & (nearby_df["acq_datetime"] <= current_time)])
            c30 = len(nearby_df[(nearby_df["acq_datetime"] >= t_30d) & (nearby_df["acq_datetime"] <= current_time)])
            c90 = len(nearby_df[(nearby_df["acq_datetime"] >= t_90d) & (nearby_df["acq_datetime"] <= current_time)])

            counts_7d.append(c7)
            counts_30d.append(c30)
            counts_90d.append(c90)

        df["hotspot_count_7d"] = counts_7d
        df["hotspot_count_30d"] = counts_30d
        df["hotspot_count_90d"] = counts_90d
        return df

firms_parser = FIRMSDataParser()
