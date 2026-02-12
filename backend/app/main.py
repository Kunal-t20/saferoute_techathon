from fastapi import FastAPI
from app.route import router
from app.database import engine, Base
from app.hazard_model import Hazard

app = FastAPI()

app.include_router(router)

Base.metadata.create_all(bind=engine)

