from pathlib import Path

import joblib

ARTIFACTS_DIR = Path(__file__).resolve().parents[2] / "artifacts"

VECTORIZER_PATH = ARTIFACTS_DIR / "vectorizer.joblib"
MODEL_PATH = ARTIFACTS_DIR / "model.joblib"


if not VECTORIZER_PATH.exists():
    raise FileNotFoundError(
        "Vectorizer artifact not found. Run the training script first."
    )

if not MODEL_PATH.exists():
    raise FileNotFoundError("Model artifact not found. Run the training script first.")

vectorizer = joblib.load(
    VECTORIZER_PATH,
)

model = joblib.load(
    MODEL_PATH,
)


message = input("Enter an SMS: ")


features = vectorizer.transform([message])


prediction = model.predict(features)


label = prediction[0]

print(f"Prediction: {label}")
