from functools import lru_cache
from pathlib import Path
import joblib


MODEL_PATH = Path(__file__).resolve().parents[2] / "models/intent_router.joblib"

@lru_cache
def load_router():
    # Only load this locally-created trusted artifact; joblib uses pickle.
    return joblib.load(MODEL_PATH)

def classify_intent(question: str) -> dict:
    model = load_router()
    scores = model.predict_proba([question]) [0]
    position = int(scores.argmax())
    label = model.classes_[position]
    confidence = float(scores[position])
    return {"label": str(label) if confidence >= 0.45 else "uncertain",
            "confidence": round(confidence, 3)}
