import pickle
import pandas as pd
from pathlib import Path

# ---------------- PATH SETUP ----------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "risk_model.pkl"
with open(MODEL_PATH, "rb") as f:
    risk_model = pickle.load(f)

FEATURE_COLUMNS = [
    "weather",
    "road_condition",
    "fatalities",
    "serious_injuries",
    "minor_injuries"
]

def predict_risk(features: dict) -> int:
    """
    features example:
    {
        "weather": 1,
        "road_condition": 0,
        "fatalities": 0,
        "serious_injuries": 2,
        "minor_injuries": 5
    }
    """

    try:
        # Ensure all required keys exist
        for col in FEATURE_COLUMNS:
            if col not in features:
                features[col] = 0

        # Arrange in correct order
        input_data = [[features[col] for col in FEATURE_COLUMNS]]

        df = pd.DataFrame(input_data, columns=FEATURE_COLUMNS)

        prediction = risk_model.predict(df)[0]

        return int(prediction)

    except Exception as e:
        print("Risk prediction error:", e)
        return 0
