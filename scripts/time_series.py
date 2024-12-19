import os
<<<<<<< HEAD

import joblib
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
=======
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import joblib
import numpy as np
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11

# Dosya yolları
PROCESSED_DATA_DIR = "./data/processed/"
MODEL_DIR = "./models/"
ENERGY_DATA_FILE = os.path.join(PROCESSED_DATA_DIR, "final_energy_data.csv")
SARIMA_MODEL_FILE = os.path.join(MODEL_DIR, "sarima_model.pkl")

# Klasör oluşturma
os.makedirs(MODEL_DIR, exist_ok=True)


def load_energy_data():
    """
    Enerji verisini yükle ve düzenli zaman serisine dönüştür.
    """
    if not os.path.exists(ENERGY_DATA_FILE):
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {ENERGY_DATA_FILE}")

    # Veriyi yükle ve yalnızca gerekli sütunları seç
    energy_data = pd.read_csv(ENERGY_DATA_FILE, parse_dates=["time"], index_col="time")
    energy_data = energy_data[["total load actual"]]  # Sadece gerekli sütun

    # Eksik değerleri doldur ve zaman serisini yeniden oluştur
<<<<<<< HEAD
    full_range = pd.date_range(
        start=energy_data.index.min(), end=energy_data.index.max(), freq="h"
    )
    energy_data = energy_data.reindex(full_range)
    energy_data.index.name = "time"
    energy_data["total load actual"] = energy_data["total load actual"].interpolate(
        method="time"
    )
=======
    full_range = pd.date_range(start=energy_data.index.min(), end=energy_data.index.max(), freq="h")
    energy_data = energy_data.reindex(full_range)
    energy_data.index.name = "time"
    energy_data["total load actual"] = energy_data["total load actual"].interpolate(method="time")
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
    return energy_data


def train_and_save_sarima_model(column="total load actual", steps=24):
    """
    SARIMA modelini eğit ve kaydet.
    """
    # Veriyi yükle
    energy_data = load_energy_data()

    # Eğitim verisini oluştur
    train = energy_data[column][:-steps]

    print("SARIMA modeli eğitiliyor, lütfen bekleyin...")

    # SARIMA modelini oluştur ve eğit
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 24))
    model_fit = model.fit(disp=False)

    # Modeli kaydet
    joblib.dump(model_fit, SARIMA_MODEL_FILE)
    print(f"SARIMA modeli başarıyla kaydedildi: {SARIMA_MODEL_FILE}")


def main():
    try:
        train_and_save_sarima_model()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")


if __name__ == "__main__":
    main()
