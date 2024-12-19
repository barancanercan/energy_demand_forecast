import os
import warnings

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.models.signature import infer_signature
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# MLflow izleme URI'sını ayarlayın
mlflow.set_tracking_uri("http://localhost:5000")

# Uyarıları kapatma
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Dosya yolları
PROCESSED_DATA_DIR = "./data/processed/"
ENERGY_DATA_FILE = PROCESSED_DATA_DIR + "final_energy_data.csv"
BEST_MODEL_DIR = "./models/"

# Klasör oluşturma
os.makedirs(BEST_MODEL_DIR, exist_ok=True)


def load_data(file_path):
    """
    İşlenmiş enerji verisini yükle.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {file_path}")
    energy_data = pd.read_csv(file_path)
    if "total load actual" not in energy_data.columns:
        raise ValueError(
            "Beklenen hedef değişken 'total load actual' veri setinde bulunamadı."
        )
    X = energy_data.drop(
        columns=["total load actual", "price actual", "time"], errors="ignore"
    )
    y = energy_data["total load actual"]
    return X, y


def train_and_log_model(model, model_name, X, y):
    """
    Modeli eğit ve MLflow ile kaydet.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # MLflow deneyi başlatma
    with mlflow.start_run():
        # Modeli eğit
        model.fit(X_train, y_train)

        # Tahminler ve metrikler
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        # Modeli kaydet
        trained_model_file = os.path.join(BEST_MODEL_DIR, f"{model_name}_model.pkl")
        joblib.dump(model, trained_model_file)
        print(f"Eğitilen model kaydedildi: {trained_model_file}")

        # MLflow ile modeli kaydet
        signature = infer_signature(X_test, predictions)
        mlflow.sklearn.log_model(model, "model", signature=signature)
        print(f"Model MLflow ile kaydedildi: {model_name}")

        # Parametreleri ve metrikleri kaydet
        mlflow.log_param("model_type", model_name)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2_score", r2)


def main():
    try:
        # Veriyi yükle
        X, y = load_data(ENERGY_DATA_FILE)

        # Modelleri dene
        models = {
            "RandomForestRegressor": RandomForestRegressor(
                n_estimators=100, random_state=42
            ),
            "XGBRegressor": XGBRegressor(n_estimators=100, random_state=42),
            "LinearRegression": LinearRegression(),
        }

        for model_name, model in models.items():
            train_and_log_model(model, model_name, X, y)

    except Exception as e:
        print(f"Bir hata oluştu: {e}")


if __name__ == "__main__":
    main()
