# src/reader.py
import pandas as pd
from pathlib import Path

def read_file(path):
    path = Path(path)

    if path.suffix == ".csv":
        return pd.read_csv(path)
    elif path.suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    else:
        raise ValueError(f"Formato no soportado: {path.suffix}")
