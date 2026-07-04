"""
extract_model.py — Run this ONCE locally to export model weights to JSON.
The JSON file is then committed so Render never needs scikit-learn.

Usage:  python extract_model.py
Output: model_weights.json
"""
import json, joblib, os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_joblib.pkl")
OUT_PATH   = os.path.join(os.path.dirname(__file__), "model_weights.json")

model = joblib.load(MODEL_PATH)

weights = {
    "coef": model.coef_[0].tolist(),          # shape: (n_features,)
    "intercept": float(model.intercept_[0]),
    "classes": model.classes_.tolist(),
    "features": ["income", "credit_score", "employment_years", "debt_to_income", "amount"]
}

with open(OUT_PATH, "w") as f:
    json.dump(weights, f, indent=2)

print(f"[OK] Saved model weights to: {OUT_PATH}")
print(f"     coef      : {weights['coef']}")
print(f"     intercept : {weights['intercept']}")
print(f"     classes   : {weights['classes']}")
