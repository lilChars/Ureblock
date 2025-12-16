# src/main.py
from reader import read_file
from processor import process_data
from writer import write_file
from data.splitXslsToCsv import split_xlsx_to_csv
import os
import shutil
import re
import pandas as pd

# Archivo de entrada
INPUT_FILE = "data/JDE Balanza de Comprobacion Octubre 2025.csv"

# Carpeta de salida de csv_pages
CSV_PAGES_DIR = "data/csv_pages"
# Archivo base para copiar formato (enero)
CSV_BASE = os.path.join(CSV_PAGES_DIR, "EDO RES ACUMULADO 2025-10 FINAL__ENERO.csv")

# Lista de meses en español
MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

# Detectar mes en el nombre del archivo de entrada
def detectar_mes(nombre):
    for mes in MESES:
        patron = re.compile(mes, re.IGNORECASE)
        if patron.search(nombre):
            return mes
    return None

# Generar variantes de nombre para el mes
def variantes_mes(mes):
    return [mes.lower(), mes.upper(), mes.capitalize()]

# Crear archivo CSV para el mes si no existe, copiando el formato de CSV_BASE
def crear_csv_mes(mes):
    base_name = "EDO RES ACUMULADO 2025-10 FINAL__"
    for variante in variantes_mes(mes):
        csv_path = os.path.join(CSV_PAGES_DIR, f"{base_name}{variante}.csv")
        if not os.path.exists(csv_path):
            # Copiar formato (solo encabezados y estructura)
            df_base = pd.read_csv(CSV_BASE, header=None)
            df_base.to_csv(csv_path, index=False, header=False)
            print(f"✔ Creado archivo para mes: {csv_path}")
        else:
            print(f"✔ Ya existe archivo para mes: {csv_path}")

mes_detectado = detectar_mes(INPUT_FILE)
if mes_detectado:
    crear_csv_mes(mes_detectado)
else:
    print("No se detectó un mes válido en el nombre del archivo de entrada.")

def main():
    # Solo generar el CSV del mes si no existe
    if mes_detectado:
        base_name = "EDO RES ACUMULADO 2025-10 FINAL__"
        variantes = variantes_mes(mes_detectado)
        faltantes = []
        for variante in variantes:
            csv_path = os.path.join(CSV_PAGES_DIR, f"{base_name}{variante}.csv")
            if not os.path.exists(csv_path):
                faltantes.append(variante)
        if faltantes:
            # Solo procesar el Excel si falta algún archivo del mes
            from data.splitXslsToCsv import split_xlsx_to_csv
            split_xlsx_to_csv()
        else:
            print(f"✔ Todos los archivos CSV del mes '{mes_detectado}' ya existen.")
    df = read_file(INPUT_FILE)
    result = process_data(df)
    print("✔ Proceso completado (solo CSV)")

if __name__ == "__main__":
    main()
