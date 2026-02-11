from fastapi import APIRouter
from app.services.heatmap_service import get_heatmap_data
from app.schema import HeatmapResponse

router = APIRouter()

@router.get("/heatmap", response_model=HeatmapResponse)
def heatmap():
    points = get_heatmap_data()
    return {"data": points}
