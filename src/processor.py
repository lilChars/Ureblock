# src/processor.py
def process_data(df):
    # limpieza mínima
    df = df.dropna(subset=["Categoria", "Monto"])

    # asegurar tipo numérico
    df["Monto"] = df["Monto"].astype(float)

    # agregación
    result = (
        df.groupby("Categoria", as_index=False)
          .agg(Total=("Monto", "sum"))
    )

    return result
