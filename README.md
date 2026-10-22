# Observatorio de sequía del Guadalquivir

Modelo de Machine Learning que predice el cambio de volumen de los embalses de la cuenca del Guadalquivir a 4 y 8 semanas, a partir del histórico de embalses (MITECO) y datos de lluvia y temperatura (AEMET).

## Objetivo
- **Regresión**: cambio de volumen (hm³) de la cuenca a 4 y 8 semanas.
- **Clasificación (extra)**: estado de la cuenca el mes siguiente (normalidad, prealerta, alerta, emergencia).

## Fuentes de datos
| Fuente | Uso |
|---|---|
| [MITECO – BD-Embalses](https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/boletin-hidrologico.html) | Histórico semanal de reservas (variable objetivo) |
| [AEMET OpenData](https://opendata.aemet.es/) | Lluvia y temperatura diarias por estación |

## Estructura
```
data/raw/          datos tal cual se descargan (no se modifican)
data/processed/    datos limpios e integrados (Parquet)
notebooks/         exploración y análisis, numerados (01_, 02_...)
src/               código reutilizable (ingesta, limpieza, features)
models/            modelos entrenados
reports/figures/   gráficas
```

## Cómo ejecutarlo
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # y poner la API key de AEMET
```

## Resultados
*(pendiente)*
