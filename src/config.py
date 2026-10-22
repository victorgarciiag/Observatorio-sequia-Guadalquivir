"""Rutas y configuración comunes del proyecto."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
MODELS = ROOT / "models"
FIGURES = ROOT / "reports" / "figures"

load_dotenv(ROOT / ".env")
AEMET_API_KEY = os.getenv("AEMET_API_KEY")
