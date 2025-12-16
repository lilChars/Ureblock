import pandas as pd

df = pd.read_excel("UNIDADES DE NEGOCIO 2025.xlsx", dtype=str)
df.to_csv("UNIDADES DE NEGOCIO 2025.csv", index=False)
# Ureblock/src/xslsToCsv.py