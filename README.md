# Observatorio de sequía del Guadalquivir

Modelo de Machine Learning que predice cuánto cambiará el volumen de agua de la cuenca del Guadalquivir en las próximas **4 semanas**, a partir de más de 30 años de datos públicos de embalses (MITECO) y de lluvia y temperatura (AEMET).

El dato actual de los embalses ya es público. El objetivo de este proyecto es **anticiparlo**: saber hacia dónde va la cuenca antes de que llegue una situación de sequía.

> Proyecto personal de aprendizaje: recorre el flujo completo de un proyecto real de ML con datos reales y sucios (ingesta, limpieza, integración, EDA, feature engineering, modelado y evaluación).

## Resultados

Error medio absoluto (MAE) prediciendo el cambio de volumen de la cuenca a 4 semanas, en el periodo de prueba 2019–2026 (sequía de 2022–2024 y borrascas de 2024–2026):

| Modelo | MAE (hm³) |
|---|---|
| Persistencia ("no cambia nada") | 174 |
| Media estacional ("lo típico de esa semana del año") | 123 |
| Regresión lineal | 124 |
| Regresión lineal + semana cíclica (seno/coseno) | 118 |
| XGBoost (ajustado con `TimeSeriesSplit`) | 114 |
| **Random Forest** | **113** |

- La cuenca tiene unos **5.900 hm³** de capacidad: 113 hm³ equivalen a unos **2 puntos de % de llenado**.
- El Random Forest mejora un **8%** a la referencia estacional, y hasta un **31%** en años de sequía (2023): ha aprendido que con poca agua se riega menos.
- **A 8 semanas no mejora** a la referencia (216 frente a 214 hm³): más allá de unas 4 semanas manda la lluvia futura, que el modelo no puede conocer.

## Qué ha enseñado el análisis de los datos

- **Estacionalidad**: la cuenca sube de noviembre a abril y baja de junio a septiembre por el riego (hasta −77 hm³ por semana en julio).
- **Memoria del sistema**: un año seco tras años húmedos no provoca sequía; las graves llegan tras varios años seguidos por debajo de lo normal (2005–2009, 2017–2024).
- **La lluvia acumulada explica mucho más que la semanal**: correlación 0,78 a 4 semanas frente a 0,51 a 1 semana. El efecto se nota sobre todo una semana después.
- **Suelo seco**: con la misma lluvia (50–100 mm en 4 semanas), la cuenca sube +31 hm³ en otoño frente a +206 hm³ en invierno.

## Datos

| Fuente | Contenido | Uso |
|---|---|---|
| [MITECO – Boletín Hidrológico (BD-Embalses)](https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/boletin-hidrologico.html) | Reserva semanal de cada embalse desde 1988 (base de datos Access, sin validar) | Variable objetivo |
| [AEMET OpenData](https://opendata.aemet.es/) | Lluvia y temperatura diarias por estación (API con clave) | Variables de clima |

Decisiones principales de la limpieza:
- **36 embalses consuntivos** (riego y abastecimiento) con datos todas las semanas desde **febrero de 1994**. Se excluyen los hidroeléctricos y los embalses que entran o salen del boletín, porque crean saltos artificiales en el total.
- Se excluye **La Breña**: en 2009 pasa de ~100 a ~823 hm³ y se llena en parte por bombeo.
- **5 estaciones de AEMET** con datos completos desde 1993 (Jaén, Córdoba, Granada, Sevilla y Morón). La lluvia de la cuenca es su media semanal, con semanas que terminan en martes como el boletín de embalses.

## Estructura

```
data/raw/          datos descargados (no se suben a Git)
data/processed/    datos limpios e integrados en Parquet (no se suben)
notebooks/         01 exploración → 02 limpieza → 03 ingesta AEMET → 04 limpieza AEMET
                   → 05 integración y EDA → 06 features → 07 modelado
src/config.py      rutas y API key (desde .env)
src/features.py    cálculo de variables, el mismo para entrenar y para predecir
src/predecir.py    predicción a 4 semanas desde la última semana disponible
models/            modelo entrenado (no se sube)
```

## Cómo ejecutarlo

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # y poner la API key de AEMET
```

1. Descargar `BD-Embalses.zip` del MITECO en `data/raw/` y exportar la tabla a CSV con mdbtools:
   ```bash
   mdb-export -T "%Y-%m-%d" data/raw/BD-Embalses.mdb "T_Datos Embalses 1988-2026" > data/raw/embalses.csv
   ```
2. Ejecutar los notebooks en orden (01 → 07). El 03 descarga los datos de AEMET (unos 20–25 minutos).
3. Predicción con el modelo guardado:
   ```bash
   python -m src.predecir
   ```

En Mac, XGBoost necesita `brew install libomp`.

## Limitaciones

- **La lluvia futura** es la mayor fuente de error: el modelo llega tarde a las borrascas y no aporta más allá de unas 4 semanas.
- **Estaciones de valle**: las estaciones de montaña, donde llueve el agua que llega a los embalses, no tienen datos antiguos.
- **Datos del boletín sin validar** y relativamente pocos datos (~1.700 semanas).
- Predice el **total de la cuenca**, no cada embalse.

## Tecnologías

Python · pandas · scikit-learn · XGBoost · matplotlib · API REST (AEMET) · mdbtools · Git

---

Datos: Ministerio para la Transición Ecológica y el Reto Demográfico (MITECO) y © AEMET.
