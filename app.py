from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

from analysis import analyze  # <-- our separate analysis module

# Load variables from .env
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)  # allows your frontend JS to call this API

# Connect to MongoDB
mongo_uri = os.getenv("MONGODB_URI")
if not mongo_uri:
    raise RuntimeError("MONGODB_URI not found. Did you create a .env file from .env.example?")

client = MongoClient(mongo_uri)
db = client["shoe_data"]
readings_collection = db["readings"]


@app.route("/readings", methods=["POST"])
def add_reading():
    """
    Accepts raw sensor data, runs it through analysis.py, and stores
    both the raw values and the computed metrics. Expects JSON like:
    {
        "device_id": "shoe_left_01",
        "pressure": 42.7,
        "gyro": {"x": 0.12, "y": -0.03, "z": 1.01},
        "frequency": 3.4
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON body received"}), 400

    metrics = analyze(data)  # -> {"form_rating": ..., "speed": ..., "suggestions": [...]}

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
    return jsonify({"status": "success", "id": str(result.inserted_id)}), 201


@app.route("/readings", methods=["GET"])
def get_readings():
    """Return the most recent readings, newest first.
    Optional query param: ?limit=50
    """
    limit = int(request.args.get("limit", 50))
    readings = list(
        readings_collection.find().sort("timestamp", -1).limit(limit)
    )
    for r in readings:
        r["_id"] = str(r["_id"])

    return jsonify(readings), 200


@app.route("/health", methods=["GET"])
def health_check():
    try:
        client.admin.command("ping")
        return jsonify({"status": "ok", "mongodb": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "mongodb": str(e)}), 500


@app.route("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
