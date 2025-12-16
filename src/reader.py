# src/reader.py
import pandas as pd
from pathlib import Path

def read_file(path):
    path = Path(path)
    if path.suffix == ".csv":
        return pd.read_csv(path)
    else:
        raise ValueError(f"Solo se soportan archivos CSV, no: {path.suffix}")
