<<<<<<< HEAD
import os
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
=======
import warnings
import pandas as pd
import numpy as np
import os
from datetime import datetime
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
PROCESSED_DATA_DIR = "./data/processed/"
ENERGY_DATA_FILE = os.path.join(RAW_DATA_DIR, "energy_dataset.csv")
WEATHER_DATA_FILE = os.path.join(RAW_DATA_DIR, "weather_features.csv")

<<<<<<< HEAD

=======
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
def load_data():
    """
    Verileri yükler ve DataFrame olarak döndürür.
    """
    energy_data = pd.read_csv(ENERGY_DATA_FILE)
    weather_data = pd.read_csv(WEATHER_DATA_FILE)
    print(f"Energy Dataset Yüklendi: {energy_data.shape}")
    print(f"Weather Dataset Yüklendi: {weather_data.shape}")
    return energy_data, weather_data


def handle_missing_values(df, threshold=0.5):
    """
    Eksik verileri doldurur veya çıkarır.

    Args:
    - df: Veri çerçevesi
    - threshold: Sütun/satır eksik oranı eşiği (default: %50)

    Returns:
    - İşlenmiş DataFrame
    """
    print(f"Orijinal veri boyutu: {df.shape}")

    # Tamamen eksik sütunları kaldır
<<<<<<< HEAD
    df = df.dropna(axis=1, how="all")
=======
    df = df.dropna(axis=1, how='all')
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11

    # Eksik satırları kaldır (eğer oran çok düşükse)
    df = df.dropna(axis=0, thresh=int(df.shape[1] * threshold))

    # Eksik değerleri uygun bir şekilde doldur
<<<<<<< HEAD
    df.fillna(method="ffill", inplace=True)  # İleri doldurma (forward fill)
    df.fillna(method="bfill", inplace=True)  # Geri doldurma (backward fill)
=======
    df.fillna(method='ffill', inplace=True)  # İleri doldurma (forward fill)
    df.fillna(method='bfill', inplace=True)  # Geri doldurma (backward fill)
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11

    print(f"İşlem sonrası veri boyutu: {df.shape}")
    return df

<<<<<<< HEAD

=======
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
def create_new_features(df):
    """
    Yeni özellikler türetir.

    Args:
    - df: Veri çerçevesi

    Returns:
    - Özellikleri genişletilmiş DataFrame
    """
    print("Yeni özellikler türetiliyor...")

    # Tarih bilgisi içeren sütunu datetime formatına çevir
<<<<<<< HEAD
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"], utc=True)
        df["hour"] = df["time"].dt.hour  # Saat bilgisi
        df["day_of_week"] = df["time"].dt.dayofweek  # Haftanın günü
        df["month"] = df["time"].dt.month  # Ay bilgisi
        df["year"] = df["time"].dt.year  # Yıl bilgisi
        df["is_weekend"] = df["time"].dt.dayofweek >= 5  # Hafta sonu mu?
        df["season"] = df["month"].apply(assign_season)  # Mevsim bilgisi

    # Enerji üretim yüzdeleri
    if "total load actual" in df.columns:
        generation_cols = [col for col in df.columns if "generation" in col]
=======
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'], utc=True)
        df['hour'] = df['time'].dt.hour  # Saat bilgisi
        df['day_of_week'] = df['time'].dt.dayofweek  # Haftanın günü
        df['month'] = df['time'].dt.month  # Ay bilgisi
        df['year'] = df['time'].dt.year  # Yıl bilgisi
        df['is_weekend'] = df['time'].dt.dayofweek >= 5  # Hafta sonu mu?
        df['season'] = df['month'].apply(assign_season)  # Mevsim bilgisi

    # Enerji üretim yüzdeleri
    if 'total load actual' in df.columns:
        generation_cols = [col for col in df.columns if 'generation' in col]
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
        total_generation = df[generation_cols].sum(axis=1)
        for col in generation_cols:
            df[f"{col}_percentage"] = (df[col] / total_generation).fillna(0) * 100

    return df


def assign_season(month):
    """
    Ay bilgisine göre mevsim belirler.
    """
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Fall"


def detect_and_handle_outliers(df):
    """
    Aykırı değerleri tespit eder ve işleme alır.
    """
    print("Aykırı değerler tespit ediliyor...")
<<<<<<< HEAD
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
=======
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Aykırı değerleri sınırlarla değiştirme
        df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
        df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])

    print("Aykırı değer işlemleri tamamlandı.")
    return df

<<<<<<< HEAD

=======
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
def outlier_summary(df):
    """
    Aykırı değerlerin sütun bazında sayısını hesaplar.
    """
<<<<<<< HEAD
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
=======
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
    outlier_counts = {}

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Aykırı değerlerin sayısını hesapla
        outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        outlier_counts[col] = outliers

    # Sonuçları bir DataFrame olarak döndür
<<<<<<< HEAD
    outlier_summary_df = pd.DataFrame(
        list(outlier_counts.items()), columns=["Column", "Outlier Count"]
    )
    return outlier_summary_df.sort_values(by="Outlier Count", ascending=False)
=======
    outlier_summary_df = pd.DataFrame(list(outlier_counts.items()), columns=['Column', 'Outlier Count'])
    return outlier_summary_df.sort_values(by='Outlier Count', ascending=False)

>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11


def save_processed_data(df, file_name):
    """
    İşlenmiş veriyi kaydeder. Gerekirse 'processed' dizinini oluşturur.
    """
    # Eğer klasör mevcut değilse oluştur
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    # İşlenmiş veriyi kaydet
    processed_file_path = os.path.join(PROCESSED_DATA_DIR, file_name)
    df.to_csv(processed_file_path, index=False)
    print(f"İşlenmiş veri kaydedildi: {processed_file_path}")


def main():
    # Veriyi yükle
    energy_data, weather_data = load_data()

    # Energy Dataset işlemleri
    print("\n=== Energy Dataset İşlemleri ===")
    energy_data = handle_missing_values(energy_data)
    energy_data = create_new_features(energy_data)

    # Aykırı değerleri kontrol etmeden önce bir özet görüntüleyelim
    print("\n=== Energy Dataset Aykırı Değer Özeti ===")
    energy_outliers = outlier_summary(energy_data)
    print(energy_outliers.to_string(index=False))  # Temiz çıktı

    # Aykırı değer işlemleri
    energy_data = detect_and_handle_outliers(energy_data)
    save_processed_data(energy_data, "processed_energy_data.csv")

    # Weather Dataset işlemleri
    print("\n=== Weather Dataset İşlemleri ===")
    weather_data = handle_missing_values(weather_data)
    weather_data = create_new_features(weather_data)

    # Aykırı değerleri kontrol etmeden önce bir özet görüntüleyelim
    print("\n=== Weather Dataset Aykırı Değer Özeti ===")
    weather_outliers = outlier_summary(weather_data)
    print(weather_outliers.to_string(index=False))  # Temiz çıktı

    # Aykırı değer işlemleri
    weather_data = detect_and_handle_outliers(weather_data)
    save_processed_data(weather_data, "processed_weather_data.csv")

    # Sadeleştirilmiş tabloyu göster
    print("\n=== İşlenmiş Veri Çerçeveleri (Sadeleştirilmiş Görünüm) ===")
    selected_energy_cols = [
<<<<<<< HEAD
        "time",
        "generation biomass",
        "generation fossil gas",
        "generation nuclear",
        "total load actual",
        "price actual",
    ]
    selected_weather_cols = [
        "dt_iso",
        "temp",
        "humidity",
        "wind_speed",
        "weather_main",
        "weather_description",
=======
        'time', 'generation biomass', 'generation fossil gas',
        'generation nuclear', 'total load actual', 'price actual'
    ]
    selected_weather_cols = [
        'dt_iso', 'temp', 'humidity', 'wind_speed',
        'weather_main', 'weather_description'
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
    ]

    simplified_energy_data = energy_data[selected_energy_cols].head()
    simplified_weather_data = weather_data[selected_weather_cols].head()

    combined_df = pd.concat(
<<<<<<< HEAD
        [
            simplified_energy_data.reset_index(drop=True),
            simplified_weather_data.reset_index(drop=True),
        ],
        axis=1,
=======
        [simplified_energy_data.reset_index(drop=True),
         simplified_weather_data.reset_index(drop=True)], axis=1
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
    )

    print(combined_df.to_string(index=False))


if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
