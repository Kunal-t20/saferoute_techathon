from fastapi import APIRouter, HTTPException

# -------- SCHEMAS --------
from app.schema import (
    HeatmapResponse,
    RouteRiskResponse,
    RouteAddressInput,
    HazardInput,
    RiskInput
)

# -------- SERVICES --------
from app.services.heatmap_service import get_heatmap_data
from app.services.route_service import calculate_route_risk
from app.services.geocode_service import geocode_address
from app.services.hazard_service import add_hazard, get_hazards
from app.services.risk_service import predict_risk

router = APIRouter()


# ================= HEATMAP =================
@router.get("/heatmap", response_model=HeatmapResponse)
def heatmap():
    points = get_heatmap_data()
    return {"data": points}


# ================= ROUTE RISK (MAIN ENDPOINT) =================
@router.post("/route-risk", response_model=RouteRiskResponse)
def route_risk(data: RouteAddressInput):
    start_coords = geocode_address(data.start)
    end_coords = geocode_address(data.end)

    if not start_coords or not end_coords:
        raise HTTPException(
            status_code=400,
            detail="Invalid start or end address"
        )

    route_points = [
        {"lat": start_coords["lat"], "lng": start_coords["lng"]},
        {"lat": end_coords["lat"], "lng": end_coords["lng"]}
    ]

    # Weather + Hazard + ML + Explanation sab
    # calculate_route_risk ke andar hota hai
    return calculate_route_risk(route_points)


# ================= GEOCODE (OPTIONAL TEST) =================
@router.get("/geocode")
def geocode(address: str):
    return geocode_address(address)


# ================= HAZARD =================
@router.post("/report-hazard")
def report_hazard(data: HazardInput):
    add_hazard(data.lat, data.lng, data.type, data.description)
    return {"status": "ok"}


@router.get("/hazards")
def hazards():
    return get_hazards()


# ================= ML RISK (DEBUG ONLY) =================
@router.post("/predict-risk")
def predict_risk_endpoint(data: RiskInput):
    score = predict_risk(data.dict())
    return {"risk_score": score}
