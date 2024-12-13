from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator, Field
import joblib
import pandas as pd
import os

app = FastAPI()

# CORS middleware'ini ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model dosyaları
MODEL_DIR = "./models/"
TRAINED_MODEL_FILE = os.path.join(MODEL_DIR, "trained_model.pkl")

# Eğitimli modeli yükle
trained_model = joblib.load(TRAINED_MODEL_FILE) if os.path.exists(TRAINED_MODEL_FILE) else None

# Giriş için gelişmiş veri modeli
class PredictionRequest(BaseModel):
    generation_biomass: float = Field(..., ge=0, le=1000)
    generation_fossil_brown_coal_lignite: float = Field(..., ge=0, le=1000)
    generation_fossil_coal_derived_gas: float = Field(..., ge=0, le=1000)
    generation_fossil_gas: float = Field(..., ge=0, le=1000)
    generation_fossil_hard_coal: float = Field(..., ge=0, le=1000)
    generation_fossil_oil: float = Field(..., ge=0, le=1000)
    generation_geothermal: float = Field(..., ge=0, le=1000)
    generation_hydro_pumped_storage_consumption: float = Field(..., ge=0, le=1000)
    generation_hydro_run_of_river_and_poundage: float = Field(..., ge=0, le=1000)
    generation_hydro_water_reservoir: float = Field(..., ge=0, le=1000)
    generation_solar: float = Field(..., ge=0, le=1000)
    generation_wind_onshore: float = Field(..., ge=0, le=1000)
    forecast_solar_day_ahead: float = Field(..., ge=0, le=1000)
    forecast_wind_onshore_day_ahead: float = Field(..., ge=0, le=1000)
    total_load_forecast: float = Field(..., ge=0, le=2000)
    hour: int = Field(..., ge=0, le=23)
    day_of_week: int = Field(..., ge=0, le=6)
    month: int = Field(..., ge=1, le=12)
    is_weekend: int = Field(..., ge=0, le=1)
    season: int = Field(..., ge=0, le=3)

    # Özel doğrulama
    @validator('is_weekend')
    def validate_weekend(cls, v):
        if v not in [0, 1]:
            raise ValueError('is_weekend sadece 0 veya 1 olabilir')
        return v

@app.get("/")
def home():
    """
    Ana sayfa rotası.
    """
    return {"message": "Enerji Tahmin API'sine Hoş Geldiniz!"}

@app.post("/predict")
def predict(request: PredictionRequest):
    """
    Enerji yükü tahmin rotası.
    """
    try:
        if not trained_model:
            raise HTTPException(status_code=500, detail="Eğitilmiş model yüklenemedi.")

        # Girdileri bir pandas DataFrame'e dönüştür
        input_data = pd.DataFrame([request.dict()])

        # Modelin eğitildiği özellikleri hizala
        trained_features = trained_model.feature_names_in_
        aligned_input = input_data.reindex(columns=trained_features, fill_value=0)

        # Tahmini yap
        prediction = trained_model.predict(aligned_input)[0]

        return {"prediction": float(prediction)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))