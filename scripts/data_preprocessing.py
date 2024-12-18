<<<<<<< HEAD
import os

import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
=======
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
import joblib
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11

# Dosya yolları
PROCESSED_DATA_DIR = "./data/processed/"
ENERGY_DATA_FILE = PROCESSED_DATA_DIR + "processed_energy_data.csv"
WEATHER_DATA_FILE = PROCESSED_DATA_DIR + "processed_weather_data.csv"
ENCODERS_DIR = "./encoders/"

# Klasör oluşturma
os.makedirs(ENCODERS_DIR, exist_ok=True)

<<<<<<< HEAD

=======
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
# RARE Encoding
def rare_encoder(data, column, threshold=0.01, replace_with="RARE"):
    """
    RARE encoding: Kategorik değişkenlerde az frekanslı kategorileri "RARE" grubuna toplar.
    """
    freq = data[column].value_counts(normalize=True)
    rare_categories = freq[freq < threshold].index.tolist()
<<<<<<< HEAD
    data[column] = data[column].apply(
        lambda x: replace_with if x in rare_categories else x
    )
    print(
        f"'{column}' sütununda {len(rare_categories)} kategori '{replace_with}' olarak yeniden adlandırıldı."
    )
    return data


=======
    data[column] = data[column].apply(lambda x: replace_with if x in rare_categories else x)
    print(f"'{column}' sütununda {len(rare_categories)} kategori '{replace_with}' olarak yeniden adlandırıldı.")
    return data

>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
# RARE Encoding Uygulama
def apply_rare_encoding(data, categorical_columns, threshold=0.01, replace_with="RARE"):
    """
    Tüm kategorik sütunlara RARE Encoding uygular. Belirli sütunlar (ör. 'time') hariç tutulur.
    """
<<<<<<< HEAD
    exclude_columns = ["time"]  # Hariç tutulacak sütunlar
    for col in categorical_columns:
        if col not in exclude_columns:
            data = rare_encoder(
                data, col, threshold=threshold, replace_with=replace_with
            )
    return data


# Kategorik ve sayısal sütunları analiz etme
def analyze_columns(data):
    categorical_cols = data.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    numerical_cols = data.select_dtypes(include=["int64", "float64"]).columns.tolist()
    return categorical_cols, numerical_cols


=======
    exclude_columns = ['time']  # Hariç tutulacak sütunlar
    for col in categorical_columns:
        if col not in exclude_columns:
            data = rare_encoder(data, col, threshold=threshold, replace_with=replace_with)
    return data

# Kategorik ve sayısal sütunları analiz etme
def analyze_columns(data):
    categorical_cols = data.select_dtypes(include=["object", "category"]).columns.tolist()
    numerical_cols = data.select_dtypes(include=["int64", "float64"]).columns.tolist()
    return categorical_cols, numerical_cols

>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
# Encoding işlemleri
def encode_columns(data, categorical_cols):
    """
    Kategorik sütunlara uygun encoding uygular (LabelEncoder, OneHotEncoder).
    """
    encoders = {}
<<<<<<< HEAD
    exclude_columns = ["time"]  # Encoding dışında tutulacak sütunlar
=======
    exclude_columns = ['time']  # Encoding dışında tutulacak sütunlar
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11

    for col in categorical_cols:
        if col in exclude_columns:
            continue  # 'time' sütununu atla

        unique_values = data[col].nunique()
        if unique_values == 2:  # İkili kategoriler için Label Encoding
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            encoders[col] = le
            joblib.dump(le, os.path.join(ENCODERS_DIR, f"{col}_label_encoder.pkl"))
        else:  # Çok kategorili değişkenler için One-Hot Encoding
<<<<<<< HEAD
            ohe = OneHotEncoder(
                sparse_output=False, handle_unknown="ignore"
            )  # 'sparse_output' kullanıldı
            ohe_features = ohe.fit_transform(data[[col]])
            ohe_feature_names = [f"{col}_{category}" for category in ohe.categories_[0]]
            ohe_df = pd.DataFrame(
                ohe_features, columns=ohe_feature_names, index=data.index
            )
=======
            ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")  # 'sparse_output' kullanıldı
            ohe_features = ohe.fit_transform(data[[col]])
            ohe_feature_names = [f"{col}_{category}" for category in ohe.categories_[0]]
            ohe_df = pd.DataFrame(ohe_features, columns=ohe_feature_names, index=data.index)
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
            data = pd.concat([data, ohe_df], axis=1)
            data.drop(columns=[col], inplace=True)
            encoders[col] = ohe
            joblib.dump(ohe, os.path.join(ENCODERS_DIR, f"{col}_onehot_encoder.pkl"))
    return data

<<<<<<< HEAD

=======
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
# Sayısal verilerin ölçeklenmesi
def scale_numeric_columns(data, numerical_cols):
    """
    Sayısal sütunları ölçeklendirme.
    """
    scaler = StandardScaler()
    data[numerical_cols] = scaler.fit_transform(data[numerical_cols])
    joblib.dump(scaler, os.path.join(ENCODERS_DIR, "numeric_scaler.pkl"))
    print("Sayısal sütunlar ölçeklendi ve scaler kaydedildi.")
    return data

<<<<<<< HEAD

=======
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
# Veri dönüşümü
def preprocess_data():
    # Veriyi yükle
    energy_data = pd.read_csv(ENERGY_DATA_FILE)
    weather_data = pd.read_csv(WEATHER_DATA_FILE)

    # Kategorik ve sayısal sütunları belirle
    energy_categorical_cols, energy_numerical_cols = analyze_columns(energy_data)
    weather_categorical_cols, weather_numerical_cols = analyze_columns(weather_data)

    # 1. RARE Encoding Uygula
    print("\nEnergy Dataset için RARE Encoding uygulanıyor...")
<<<<<<< HEAD
    energy_data = apply_rare_encoding(
        energy_data, energy_categorical_cols, threshold=0.01
    )
    print("\nWeather Dataset için RARE Encoding uygulanıyor...")
    weather_data = apply_rare_encoding(
        weather_data, weather_categorical_cols, threshold=0.01
    )
=======
    energy_data = apply_rare_encoding(energy_data, energy_categorical_cols, threshold=0.01)
    print("\nWeather Dataset için RARE Encoding uygulanıyor...")
    weather_data = apply_rare_encoding(weather_data, weather_categorical_cols, threshold=0.01)
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11

    # 2. Encoding işlemleri
    print("\nEnergy Dataset için dönüşümler uygulanıyor...")
    energy_data = encode_columns(energy_data, energy_categorical_cols)
    energy_data = scale_numeric_columns(energy_data, energy_numerical_cols)

    print("\nWeather Dataset için dönüşümler uygulanıyor...")
    weather_data = encode_columns(weather_data, weather_categorical_cols)
    weather_data = scale_numeric_columns(weather_data, weather_numerical_cols)

    # İşlenmiş verileri kaydet
<<<<<<< HEAD
    energy_data.to_csv(
        os.path.join(PROCESSED_DATA_DIR, "final_energy_data.csv"), index=False
    )
    weather_data.to_csv(
        os.path.join(PROCESSED_DATA_DIR, "final_weather_data.csv"), index=False
    )
    print("İşlenmiş veriler kaydedildi.")


def main():
    preprocess_data()


=======
    energy_data.to_csv(os.path.join(PROCESSED_DATA_DIR, "final_energy_data.csv"), index=False)
    weather_data.to_csv(os.path.join(PROCESSED_DATA_DIR, "final_weather_data.csv"), index=False)
    print("İşlenmiş veriler kaydedildi.")

def main():
    preprocess_data()

>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
if __name__ == "__main__":
    main()
