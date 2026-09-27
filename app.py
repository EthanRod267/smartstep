from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
from typing import Optional, List

from analysis import analyze  # unchanged from the Flask version

# ---- Load environment variables ----
load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")
if not mongo_uri:
    raise RuntimeError("MONGODB_URI not found. Did you create a .env file from .env.example?")

client = MongoClient(mongo_uri)
db = client["shoe_data"]
readings_collection = db["readings"]

# ---- FastAPI app setup ----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # fine for a competition demo; tighten for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve everything in static/ at /static/... (same URL pattern as the Flask version)
app.mount("/static", StaticFiles(directory="static"), name="static")


# ---- Request/response models (this is the validation FastAPI adds for free) ----
class Gyro(BaseModel):
    x: float
    y: float
    z: float


class SensorReading(BaseModel):
    device_id: str = "unknown"
    pressure: Optional[float] = None
    gyro: Optional[Gyro] = None
    frequency: Optional[float] = None


# ---- Routes ----
@app.post("/readings", status_code=201)
def add_reading(reading_in: SensorReading):
    data = reading_in.dict()
    metrics = analyze(data)  # same analysis.py, no changes needed

    reading = {
        "device_id": data.get("device_id", "unknown"),
        "pressure": data.get("pressure"),
        "gyro": data.get("gyro"),
        "frequency": data.get("frequency"),
        "form_rating": metrics["form_rating"],
        "speed": metrics["speed"],
        "suggestions": metrics["suggestions"],
        "timestamp": datetime.utcnow().isoformat()
    }

    result = readings_collection.insert_one(reading)
    return {"status": "success", "id": str(result.inserted_id)}


@app.get("/readings")
def get_readings(limit: int = 50):
    readings = list(
        readings_collection.find().sort("timestamp", -1).limit(limit)
    )
    for r in readings:
        r["_id"] = str(r["_id"])
    return readings


@app.get("/health")
def health_check():
    try:
        client.admin.command("ping")
        return {"status": "ok", "mongodb": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"mongodb error: {e}")


@app.get("/")
def index():
    return FileResponse("static/index.html")


# No if __name__ == "__main__" block needed —
# FastAPI apps are run with uvicorn (see instructions below).
