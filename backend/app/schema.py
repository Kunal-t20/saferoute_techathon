from pydantic import BaseModel
from typing import List,Optional

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


class HazardInput(BaseModel):
    lat: float
    lng: float
    type: str
    description: str

class RiskInput(BaseModel):
    weather: int
    road_condition: int
    fatalities: int
    serious_injuries: int
    minor_injuries: int

class RouteRiskResponse(BaseModel):
    risk_percentage: int
    level: str
    hotspot_hits: int
    hazard_hits: int
    weather: str
    explanation: Optional[str] = None