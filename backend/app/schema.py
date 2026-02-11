from pydantic import BaseModel
from typing import List

# ---------- HEATMAP ----------
class HeatmapPoint(BaseModel):
    lat: float
    lng: float
    intensity: int
    risk: str


class HeatmapResponse(BaseModel):
    data: List[HeatmapPoint]


# ---------- ROUTE RISK ----------
class Point(BaseModel):
    lat: float
    lng: float

class RouteAddressInput(BaseModel):
    start: str
    end: str



class RouteInput(BaseModel):
    points: List[Point]


class RouteRiskResponse(BaseModel):
    risk_percentage: int
    level: str
    hotspot_hits: int
