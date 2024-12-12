import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
import numpy as np
import warnings

# Uyarıları kapat
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Veri yükleme
PROCESSED_DATA_DIR = "./data/processed/"
ENERGY_DATA_FILE = PROCESSED_DATA_DIR + "final_energy_data.csv"


def load_data():
    """
    İşlenmiş enerji verisini yükle ve düzenli zaman serisine dönüştür.
    """
    energy_data = pd.read_csv(ENERGY_DATA_FILE, parse_dates=["time"], index_col="time")

    # Tüm zaman aralığını tamamlamak için yeniden indeksleme
    full_range = pd.date_range(start=energy_data.index.min(), end=energy_data.index.max(), freq="H")
    energy_data = energy_data.reindex(full_range)
    energy_data.index.name = "time"

    return energy_data


def plot_time_series(df, columns, title="Time Series Data"):
    """
    Zaman serisini görselleştir.
    """
    plt.figure(figsize=(12, 6))
    for col in columns:
        plt.plot(df.index, df[col], label=col)
    plt.title(title, fontsize=16)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Values", fontsize=12)
    plt.legend()
    plt.grid()
    plt.show()


def seasonal_analysis(df, column):
    """
    Mevsimsel analiz yap ve çiz.
    """
    df = df.dropna(subset=[column])  # Eksik değerleri kaldır
    result = seasonal_decompose(df[column], model="additive", period=24 * 7)
    result.plot()
    plt.tight_layout()
    plt.show()


def sarima_forecast(df, column, steps=24):
    """
    SARIMA model kullanarak tahmin yap.
    """
    # Eksik değerleri doldur
    df[column] = df[column].interpolate(method="time")

    # Eğitim ve test setlerini oluştur
    train = df[column][:-steps]
    test = df[column][-steps:]

    # Modeli tanımla ve eğit
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 24))
    model_fit = model.fit(disp=False)

    # Tahmin yap
    forecast = model_fit.forecast(steps=steps)

    # Performansı değerlendir
    mse = mean_squared_error(test, forecast)
    print(f"{column} için Tahmin Hatası (MSE): {mse:.2f}")

    # Sonuçları çiz
    plt.figure(figsize=(12, 6))
    plt.plot(df.index[-2 * steps:], df[column][-2 * steps:], label="Gerçek Değerler")
    plt.plot(df.index[-steps:], forecast, label="Tahminler", linestyle="--")
    plt.title(f"SARIMA Tahmini: {column}", fontsize=16)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Values", fontsize=12)
    plt.legend()
    plt.grid()
    plt.show()


def main():
    # Veriyi yükle
    energy_data = load_data()

    # 1. Zaman Serisi Görselleştirme
    plot_time_series(energy_data, columns=["total load actual", "price actual"], title="Electricity Load and Price")

    # 2. Mevsimsel Analiz
    seasonal_analysis(energy_data, column="total load actual")

    # 3. SARIMA Tahmini
    sarima_forecast(energy_data, column="total load actual", steps=24)


if __name__ == "__main__":
    main()
