"""Variables del modelo. Se usa igual para entrenar y para predecir."""
import numpy as np
import pandas as pd

FEATURES = [
    "volumen", "pct_llenado", "cambio_1s", "cambio_4s",
    "lluvia", "lluvia_lag1", "lluvia_4s", "lluvia_12s", "lluvia_26s",
    "lluvia_año_hidro", "semana", "tmed", "tmed_4s",
]
COLUMNAS = FEATURES + ["sem_sin", "sem_cos"]
OBJETIVOS = ["objetivo_4s", "objetivo_8s"]


def crear_features(dataset: pd.DataFrame) -> pd.DataFrame:
    """Recibe el dataset semanal (clima + cuenca, índice = fecha de los martes)
    y devuelve las variables del modelo y los objetivos a 4 y 8 semanas."""
    df = dataset.copy()

    # Memoria del embalse
    df["cambio_1s"] = df["volumen"].diff(1)
    df["cambio_4s"] = df["volumen"].diff(4)

    # Lluvia reciente y acumulada
    df["lluvia_lag1"] = df["lluvia"].shift(1)
    for n in [4, 12, 26]:
        df[f"lluvia_{n}s"] = df["lluvia"].rolling(n).sum()

    # Estado del suelo: lluvia desde el 1 de octubre
    año_hidro = df.index.year + (df.index.month >= 10)
    df["lluvia_año_hidro"] = df.groupby(año_hidro)["lluvia"].cumsum()

    # Estacionalidad (también cíclica) y calor
    df["semana"] = df.index.isocalendar().week.astype(int)
    df["sem_sin"] = np.sin(2 * np.pi * df["semana"] / 52)
    df["sem_cos"] = np.cos(2 * np.pi * df["semana"] / 52)
    df["tmed_4s"] = df["tmed"].rolling(4).mean()

    # Objetivos (lo único que mira al futuro)
    df["objetivo_4s"] = df["volumen"].shift(-4) - df["volumen"]
    df["objetivo_8s"] = df["volumen"].shift(-8) - df["volumen"]

    return df[df["volumen"].notna()]
