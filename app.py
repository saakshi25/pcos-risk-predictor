from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("models/pcos_model_modified.pkl")
features = joblib.load("models/features_modified.pkl")
feature_means = joblib.load("models/feature_means.pkl")


@app.get("/")
def home():
    return {"message": "PCOS Prediction API running"}

@app.post("/predict")
def predict(data: dict):

    try:
        input_data = {}

        for f in features:
            input_data[f] = data.get(f, feature_means[f])

        input_df = pd.DataFrame([input_data])

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        return {
            "prediction": int(prediction),
            "probability": float(probability)
        }

    except Exception as e:
        return {"error": str(e)}