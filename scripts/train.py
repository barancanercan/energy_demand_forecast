import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import joblib
import warnings

# Uyarıları kapatma
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Dosya yolları
PROCESSED_DATA_DIR = "./data/processed/"
ENERGY_DATA_FILE = PROCESSED_DATA_DIR + "final_energy_data.csv"
BEST_MODEL_DIR = "./models/"
BEST_MODEL_FILE = os.path.join(BEST_MODEL_DIR, "XGBoost_best_model.pkl")
TRAINED_MODEL_FILE = os.path.join(BEST_MODEL_DIR, "trained_model.pkl")

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
        raise ValueError("Beklenen hedef değişken 'total load actual' veri setinde bulunamadı.")
    X = energy_data.drop(columns=["total load actual", "price actual", "time"], errors="ignore")
    y = energy_data["total load actual"]
    return X, y


def load_best_model():
    """
    En iyi modeli yükle.
    """
    if not os.path.exists(BEST_MODEL_FILE):
        raise FileNotFoundError(f"En iyi model dosyası bulunamadı: {BEST_MODEL_FILE}")
    model = joblib.load(BEST_MODEL_FILE)
    print(f"En iyi model yüklendi: {BEST_MODEL_FILE}")
    return model


def train_and_save_model(model, X, y):
    """
    Verilen modelle tam veri üzerinde eğitimi yap ve modeli kaydet.
    """
    print("Model eğitimi başlatılıyor...")
    model.fit(X, y)
    print("Model eğitimi tamamlandı.")

    # Eğitilen modeli kaydet
    joblib.dump(model, TRAINED_MODEL_FILE)
    print(f"Eğitilen model kaydedildi: {TRAINED_MODEL_FILE}")


def main():
    try:
        # Veriyi yükle
        X, y = load_data(ENERGY_DATA_FILE)

        # En iyi modeli yükle
        best_model = load_best_model()

        # Modeli eğit ve kaydet
        train_and_save_model(best_model, X, y)

    except Exception as e:
        print(f"Bir hata oluştu: {e}")


if __name__ == "__main__":
    main()
