import os
<<<<<<< HEAD

=======
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
import joblib
import pandas as pd

# Dosya yolları
PROCESSED_DATA_DIR = "./data/processed/"
ENERGY_DATA_FILE = PROCESSED_DATA_DIR + "final_energy_data.csv"
TRAINED_MODEL_FILE = "./models/trained_model.pkl"


def load_trained_model():
    """
    Eğitilmiş modeli yükler ve eğitim sırasında kullanılan özellikleri kontrol eder.
    """
    if not os.path.exists(TRAINED_MODEL_FILE):
<<<<<<< HEAD
        raise FileNotFoundError(
            f"Eğitilmiş model dosyası bulunamadı: {TRAINED_MODEL_FILE}"
        )
=======
        raise FileNotFoundError(f"Eğitilmiş model dosyası bulunamadı: {TRAINED_MODEL_FILE}")
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
    model = joblib.load(TRAINED_MODEL_FILE)
    print(f"Eğitilmiş model yüklendi: {TRAINED_MODEL_FILE}")
    return model


def align_features(test_data, trained_features):
    """
    Test verisini eğitilmiş modelin özellikleriyle hizalar.
    """
    # Eksik özellikleri sıfırla doldur
    for feature in trained_features:
        if feature not in test_data:
            test_data[feature] = 0

    # Fazla özellikleri kaldır
    test_data = test_data[trained_features]
    return test_data


def predict_sample(model, sample):
    """
    Yeni bir örnek girdi için tahmin yapar.
    """
    # Modelin kullandığı özellikleri al
    trained_features = model.feature_names_in_

    # Test verisini hizala
    sample_df = pd.DataFrame([sample])
    aligned_sample = align_features(sample_df, trained_features)

    # Tahmin yap
    prediction = model.predict(aligned_sample)
    print(f"Tahmin edilen toplam yük: {prediction[0]:.4f}")
    return prediction[0]


def main():
    try:
        # Eğitilmiş modeli yükle
        model = load_trained_model()

        # Yeni bir örnek girdi
        example_input = {
            "generation biomass": 200,
            "generation fossil brown coal/lignite": 400,
            "generation fossil coal-derived gas": 0,
            "generation fossil gas": 5000,
            "generation fossil hard coal": 4800,
            "generation fossil oil": 150,
            "generation geothermal": 800,
            "generation hydro pumped storage consumption": 1000,
            "generation hydro run-of-river and poundage": 1200,
            "generation hydro water reservoir": 2500,
            "generation solar": 300,
            "generation wind onshore": 6000,
            "forecast solar day ahead": 200,
            "forecast wind onshore day ahead": 5500,
            "total load forecast": 26000,
            "hour": 15,
            "day_of_week": 2,
            "month": 12,
            "is_weekend": 0,
<<<<<<< HEAD
            "season": 3,
=======
            "season": 3
>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
        }

        # Tahmin yap
        predict_sample(model, example_input)

    except Exception as e:
        print(f"Bir hata oluştu: {e}")


if __name__ == "__main__":
    main()
<<<<<<< HEAD
=======


>>>>>>> 0a8cd4ce9a1540d36467328972bb58442e644d11
