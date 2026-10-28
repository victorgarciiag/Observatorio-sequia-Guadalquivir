"""Predice el cambio de volumen de la cuenca a 4 semanas desde la última semana disponible.

Uso (desde la raíz del proyecto):  python -m src.predecir
"""
import joblib
import pandas as pd

from src.config import DATA_PROCESSED, MODELS
from src.features import COLUMNAS, crear_features

MAE_TEST = 113  # error medio del modelo en 2019-2026 (hm³)


def main():
    dataset = pd.read_parquet(DATA_PROCESSED / "dataset_semanal.parquet")
    modelo = joblib.load(MODELS / "rf_objetivo_4s.joblib")

    hoy = crear_features(dataset).iloc[[-1]]
    volumen = hoy["volumen"].iloc[0]
    capacidad = volumen / hoy["pct_llenado"].iloc[0] * 100
    cambio = modelo.predict(hoy[COLUMNAS])[0]

    print("Fecha:", hoy.index[0].date())
    print(f"Volumen actual: {volumen:.0f} hm³ ({volumen / capacidad:.1%})")
    print(f"Cambio previsto en 4 semanas: {cambio:+.0f} hm³ (error típico ±{MAE_TEST})")
    print(f"Volumen previsto: {volumen + cambio:.0f} hm³ ({(volumen + cambio) / capacidad:.1%})")


if __name__ == "__main__":
    main()
