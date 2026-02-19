import joblib
import pandas as pd
from pathlib import Path

# ---------- PATH ----------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ML" / "risk_model.pkl"

# ---------- GLOBAL MODEL ----------
risk_model = None


def get_model():
    """
    Lazy-load model safely.
    """
    global risk_model

    if risk_model is None:
        try:
            risk_model = joblib.load(MODEL_PATH)
            print("Risk model loaded.")
        except Exception as e:
            print("Model load error:", e)
            risk_model = None

    return risk_model


def predict_risk(features: dict) -> int:
    """
    Predict risk score (0–100).
    """

    try:
        model = get_model()

        if model is None:
            return 0

        # dict → dataframe
        df = pd.DataFrame([features])

        # align columns safely
        if hasattr(model, "feature_names_in_"):
            df = df.reindex(
                columns=model.feature_names_in_,
                fill_value=0
            )

        # ==================================================
        # PROBABILITY BASED OUTPUT (BEST)
        # ==================================================
        if hasattr(model, "predict_proba"):

            probs = model.predict_proba(df)[0]

            # safer class handling
            if hasattr(model, "classes_"):
                classes = list(model.classes_)

                # assume highest class = higher risk
                risk_class_index = len(classes) - 1
                prob = probs[risk_class_index]
            else:
                prob = probs[-1]

            return int(prob * 100)

        # ==================================================
        # FALLBACK
        # ==================================================
        pred = model.predict(df)[0]

        # convert binary prediction → percentage
        if isinstance(pred, (int, float)):
            return int(float(pred) * 100)

        return 0

    except Exception as e:
        print("Risk prediction error:", e)
        return 0
