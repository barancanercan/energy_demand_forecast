<<<<<<< HEAD
import os
import warnings

import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd
=======
import warnings
import pandas as pd
import missingno as msno
import os
import matplotlib.pyplot as plt
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11

# Tüm uyarıları kapat
warnings.filterwarnings("ignore")

<<<<<<< HEAD
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", lambda x: "%.3f" % x)
pd.set_option("display.width", 500)
=======
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 500)
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11


# Dosya yolları
RAW_DATA_DIR = "./data/raw/"
ENERGY_DATA_FILE = os.path.join(RAW_DATA_DIR, "energy_dataset.csv")
WEATHER_DATA_FILE = os.path.join(RAW_DATA_DIR, "weather_features.csv")


def load_data():
    """
    Verileri yükler ve DataFrame olarak döndürür.
    """
    energy_data = pd.read_csv(ENERGY_DATA_FILE)
    weather_data = pd.read_csv(WEATHER_DATA_FILE)
    return energy_data, weather_data


def analyze_missing_values(df, name="Dataset"):
    """
    Eksik değer analizi.
    """
    print(f"==== {name} Missing Values ====")
    print(df.isnull().sum())
    msno.matrix(df)
    plt.title(f"{name} - Missing Data Matrix")
    plt.tight_layout()
    plt.show()


def analyze_correlation(df, name="Dataset"):
    """
    Korelasyon analizi ve düzenlenmiş çıktıyı döndürme.
    """
    print(f"==== {name} Correlation Analysis ====")

    # Sadece sayısal sütunları seç
    numeric_df = df.select_dtypes(include=["int64", "float64"])

    # Korelasyon matrisini hesapla
    corr = numeric_df.corr()

    # Matris değerlerini düzenle (ondalık basamak, NaN değerleri "N/A" ile değiştir)
    corr = corr.round(2).fillna("N/A")

    # Daha okunabilir formatta yazdır
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(corr)

    # Matrisin kendisini döndür
    return corr


def analyze_categorical(df, name="Dataset"):
    """
    Kategorik verilerin analizini yapar.
    """
    print(f"==== {name} Categorical Analysis ====")
    categorical_cols = df.select_dtypes(include=["object"]).columns
    print(f"Kategorik Kolonlar: {list(categorical_cols)}\n")

    for col in categorical_cols:
        print(f"-- {col} --")
        print(df[col].value_counts())
        print("\n")


def analyze_time_series(df, time_column, name="Dataset"):
    """
    Zaman serisi özelliklerini analiz eder.
    """
    print(f"==== {name} Time Series Analysis ====")
    if time_column in df.columns:
        # Zaman sütununu datetime formatına çevir ve UTC'ye ayarla
        df[time_column] = pd.to_datetime(df[time_column], utc=True)

        # Zaman sütununu indeks olarak ayarla
        df.set_index(time_column, inplace=True)

        # Aylık ortalamaları çiz
<<<<<<< HEAD
        df.resample("ME").mean().plot(figsize=(12, 6), title=f"{name} Monthly Mean")
=======
        df.resample('ME').mean().plot(figsize=(12, 6), title=f"{name} Monthly Mean")
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
        plt.xlabel("Tarih")
        plt.ylabel("Ortalama Değerler")
        plt.tight_layout()
        plt.show()
    else:
        print(f"{time_column} sütunu bulunamadı.")


def main():
    # Veri yükleme
    energy_data, weather_data = load_data()

    # Energy Dataset Analizi
    analyze_missing_values(energy_data, name="Energy Data")
    analyze_correlation(energy_data, name="Energy Data")
    analyze_categorical(energy_data, name="Energy Data")
    analyze_time_series(energy_data, time_column="time", name="Energy Data")

    # Weather Dataset Analizi
    analyze_missing_values(weather_data, name="Weather Data")
    analyze_correlation(weather_data, name="Weather Data")
    analyze_categorical(weather_data, name="Weather Data")


if __name__ == "__main__":
    main()
