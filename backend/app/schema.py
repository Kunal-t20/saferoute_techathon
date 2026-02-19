from pydantic import BaseModel
from typing import List, Optional


# ==================================================
# HEATMAP
# ==================================================
class HeatmapPoint(BaseModel):
    lat: float
    lng: float
    intensity: int
    risk: str
    type: Optional[str] = None   # ⭐ IMPORTANT


class HeatmapResponse(BaseModel):
    data: List[HeatmapPoint]


# ==================================================
# ROUTE INPUTS
# ==================================================
class Point(BaseModel):
    lat: float
    lng: float


class RouteAddressInput(BaseModel):
    start: str
    end: str


class RouteInput(BaseModel):
    points: List[Point]


# ==================================================
# HAZARD
# ==================================================
class HazardInput(BaseModel):
    lat: float
    lng: float
    type: str
    description: str


# ==================================================
# ML RISK DEBUG INPUT
# ==================================================
class RiskInput(BaseModel):
    weather: int
    road_condition: int
    fatalities: int
    serious_injuries: int
    minor_injuries: int


# ==================================================
# ROUTE RISK RESPONSE
# ==================================================
class RouteRiskResponse(BaseModel):
    risk_percentage: int
    level: str
    hotspot_hits: int
    hazard_hits: int
    weather: str
    explanation: Optional[str] = None

    # map markers
    start_lat: float
    start_lng: float
    end_lat: float
    end_lng: float

    route_path: List[Point]
