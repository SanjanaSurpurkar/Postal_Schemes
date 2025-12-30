from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# -----------------------------
# Load CSV DATA (same as Model.ipynb)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "post_office_schemes (1).csv")

try:
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip().str.lower()
except Exception as e:
    print("CSV load error:", e)
    df = pd.DataFrame()

# -----------------------------
# Health Check
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Backend running",
        "records_loaded": len(df)
    })

# -----------------------------
# SEARCH API (REAL LOGIC)
# -----------------------------
@app.route("/search", methods=["POST"])
def search_scheme():
    data = request.json

    state = data.get("state", "").lower().strip()
    city = data.get("city", "").lower().strip()
    post_office = data.get("postOffice", "").lower().strip()

    if df.empty:
        return jsonify({
            "success": False,
            "message": "Dataset not loaded"
        }), 500

    filtered = df.copy()

    # 🔹 Same filtering logic as notebook
    if state:
        filtered = filtered[filtered["state"].str.lower() == state]

    if city:
        filtered = filtered[filtered["district"].str.lower() == city]

    if post_office:
        filtered = filtered[
            filtered["post office"].str.lower().str.contains(post_office)
        ]

    if filtered.empty:
        return jsonify({
            "success": False,
            "message": "No matching post offices found",
            "results": []
        })

    # Limit response (important)
    results = filtered.head(15).to_dict(orient="records")

    return jsonify({
        "success": True,
        "count": len(results),
        "results": results
    })

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
