from app.database import SessionLocal
from app.hazard_model import Hazard

def add_hazard(lat, lng, hazard_type, description):
    db = SessionLocal()
    hazard = Hazard(
        latitude=lat,
        longitude=lng,
        type=hazard_type,
        description=description
    )
    db.add(hazard)
    db.commit()
    db.close()

def get_hazards():
    db = SessionLocal()
    hazards = db.query(Hazard).all()
    db.close()

    return [
        {
            "lat": h.latitude,
            "lng": h.longitude,
            "type": h.type,
            "description": h.description
        }
        for h in hazards
    ]
