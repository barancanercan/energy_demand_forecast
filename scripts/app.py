from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# FastAPI uygulamasını oluştur
app = FastAPI()

# Eğitimli modeli yükle
MODEL_PATH = "./models/trained_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Eğitilmiş model dosyası bulunamadı: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

# Giriş için veri modeli tanımla
class PredictionRequest(BaseModel):
    generation_biomass: float
    generation_fossil_brown_coal_lignite: float
    generation_fossil_coal_derived_gas: float
    generation_fossil_gas: float
    generation_fossil_hard_coal: float
    generation_fossil_oil: float
    generation_geothermal: float
    generation_hydro_pumped_storage_consumption: float
    generation_hydro_run_of_river_and_poundage: float
    generation_hydro_water_reservoir: float
    generation_solar: float
    generation_wind_onshore: float
    forecast_solar_day_ahead: float
    forecast_wind_onshore_day_ahead: float
    total_load_forecast: float
    hour: int
    day_of_week: int
    month: int
    is_weekend: int
    season: int


@app.get("/")
def home():
    """
    Ana sayfa rotası.
    """
    return {"message": "Enerji Tahmin API'sine Hoş Geldiniz!"}


@app.post("/predict")
@app.post("/predict")
def predict(request: PredictionRequest):
    """
    Tahmin rotası.
    """
    try:
        # Girdileri bir pandas DataFrame'e dönüştür
        input_data = pd.DataFrame([request.dict()])

        # Modelin eğitildiği özellikleri hizala
        trained_features = model.feature_names_in_
        aligned_input = input_data.reindex(columns=trained_features, fill_value=0)

        # Tahmini yap
        prediction = model.predict(aligned_input)[0]

        # Tahmin sonucunu float tipine dönüştür
        return {"prediction": float(prediction)}

    except Exception as e:
        return {"error": str(e)}
