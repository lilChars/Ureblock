# src/writer.py
from pathlib import Path

def write_file(df, path):
    path = Path(path)

    if path.suffix == ".csv":
        df.to_csv(path, index=False)
    elif path.suffix == ".xlsx":
        df.to_excel(path, index=False)
    else:
        raise ValueError("Formato de salida no soportado")
