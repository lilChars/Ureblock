import pandas as pd

df = pd.read_excel("CATALOGO CUENTAS GRAL.xlsx", dtype=str)
df.to_csv("CATALOGO CUENTAS GRAL.csv", index=False)
# Ureblock/src/xslsToCsv.py