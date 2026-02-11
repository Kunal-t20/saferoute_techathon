from pydantic import BaseModel
from typing import List

class HeatmapPoint(BaseModel):
    lat: float
    lng: float
    intensity: int
    risk: str


class HeatmapResponse(BaseModel):
    data: List[HeatmapPoint]
