import os
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, train_test_split
from xgboost import XGBRegressor

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


def custom_xgboost_grid_search(X, y, param_grid):
    """
    XGBoost için manuel grid search
    """
    best_params = None
    best_score = float("inf")

    for n_estimators in param_grid["n_estimators"]:
        for learning_rate in param_grid["learning_rate"]:
            for max_depth in param_grid["max_depth"]:
                model = XGBRegressor(
                    n_estimators=n_estimators,
                    learning_rate=learning_rate,
                    max_depth=max_depth,
                    random_state=42,
                )

                # Cross-validation skorunu hesapla
                scores = []
                for train_index, val_index in _custom_kfold(X):
                    X_train, X_val = X.iloc[train_index], X.iloc[val_index]
                    y_train, y_val = y.iloc[train_index], y.iloc[val_index]

                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_val)
                    score = mean_squared_error(y_val, y_pred)
                    scores.append(score)

                mse = np.mean(scores)

                print(
                    f"Params - n_est: {n_estimators}, lr: {learning_rate}, depth: {max_depth}, MSE: {mse:.4f}"
                )

                if mse < best_score:
                    best_score = mse
                    best_params = {
                        "n_estimators": n_estimators,
                        "learning_rate": learning_rate,
                        "max_depth": max_depth,
                    }

    return best_params, best_score


def _custom_kfold(X, n_splits=3):
    """
    Manuel K-Fold cross-validation için yardımcı fonksiyon
    """
    from sklearn.model_selection import KFold

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    return kf.split(X)


def hyperparameter_optimization(X, y):
    """
    Birkaç model ve parametre üzerinde hiperparametre optimizasyonu yapar.
    """
    # Eğitim ve doğrulama setlerini ayır
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model ve parametre listesi
    from sklearn.model_selection import GridSearchCV

    rf_model = RandomForestRegressor(random_state=42)
    rf_param_grid = {
        "n_estimators": [50, 100, 200],
        "max_depth": [10, 20, 30],
        "min_samples_split": [2, 5, 10],
    }

    xgb_param_grid = {
        "learning_rate": [0.01, 0.1, 0.2],
        "n_estimators": [50, 100, 200],
        "max_depth": [3, 5, 7],
    }

    best_model = None
    best_score = float("inf")
    best_model_name = None

    # RandomForest Grid Search
    grid_search = GridSearchCV(
        estimator=rf_model,
        param_grid=rf_param_grid,
        scoring="neg_mean_squared_error",
        cv=3,
        verbose=1,
        n_jobs=-1,
    )
    grid_search.fit(X_train, y_train)

    rf_best_params = grid_search.best_params_
    rf_best_model = grid_search.best_estimator_
    rf_val_predictions = rf_best_model.predict(X_val)
    rf_val_score = mean_squared_error(y_val, rf_val_predictions)

    print(f"\nRandomForest En iyi parametreler: {rf_best_params}")
    print(f"RandomForest Doğrulama Hatası (MSE): {rf_val_score:.4f}")

    best_score = rf_val_score
    best_model = rf_best_model
    best_model_name = "RandomForest"

    # XGBoost Manuel Grid Search
    print(f"\n{'=' * 20}\nModel: XGBoost\n{'=' * 20}")
    try:
        xgb_best_params, xgb_score = custom_xgboost_grid_search(
            X_train, y_train, xgb_param_grid
        )

        xgb_model = XGBRegressor(**xgb_best_params, random_state=42)
        xgb_model.fit(X_train, y_train)
        xgb_val_predictions = xgb_model.predict(X_val)
        xgb_val_score = mean_squared_error(y_val, xgb_val_predictions)

        print(f"XGBoost En iyi parametreler: {xgb_best_params}")
        print(f"XGBoost Doğrulama Hatası (MSE): {xgb_val_score:.4f}")

        if xgb_val_score < best_score:
            best_score = xgb_val_score
            best_model = xgb_model
            best_model_name = "XGBoost"
    except Exception as e:
        print(f"XGBoost modeliyle ilgili bir hata oluştu: {e}")
        import traceback

        traceback.print_exc()

    print(f"\nEn iyi model: {best_model_name} (MSE: {best_score:.4f})")
    return best_model, best_model_name


def save_best_model(model, model_name):
    """
    En iyi modeli kaydeder.
    """
    model_path = os.path.join(BEST_MODEL_DIR, f"{model_name}_best_model.pkl")
    joblib.dump(model, model_path)
    print(f"En iyi model kaydedildi: {model_path}")


def main():
    try:
        # Veriyi yükle
        X, y = load_data(ENERGY_DATA_FILE)

        # Hiperparametre optimizasyonu
        best_model, best_model_name = hyperparameter_optimization(X, y)

        # En iyi modeli kaydet
        save_best_model(best_model, best_model_name)

    except Exception as e:
        print(f"Bir hata oluştu: {e}")


if __name__ == "__main__":
    main()

"""

RandomForest En iyi parametreler:

max_depth: 30
min_samples_split: 2
n_estimators: 200
Doğrulama Hatası (MSE): 0.0078
XGBoost En iyi parametreler:

n_estimators: 200
learning_rate: 0.2
max_depth: 7
Doğrulama Hatası (MSE): 0.0043

"""
