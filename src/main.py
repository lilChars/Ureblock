# Detectar mes en el nombre del archivo de entrada
def detectar_mes(nombre):
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    for mes in meses:
        if mes in nombre.lower():
            return mes
    return None
# --- Import dinámico para split_xlsx_to_csv (para uso en crear_csv_mes) ---
import sys
import os
import csv
from pathlib import Path

# Definición de rutas globales necesarias
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INPUT_FILE = os.path.join(BASE_DIR, "data/JDE Balanza de Comprobacion Octubre 2025.csv")
CSV_PAGES_DIR = os.path.join(BASE_DIR, "data/csv_pages")
CSV_BASE = os.path.join(CSV_PAGES_DIR, "EDO RES ACUMULADO 2025-10 FINAL__ENERO.csv")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')))
from splitXslsToCsv import split_xlsx_to_csv
import shutil
import re
import pandas as pd

CSV_BUSSINES = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/UNIDADES DE NEGOCIO 2025.csv'))
def cargar_diccionario_codigos(csv_path):
    if not os.path.exists(csv_path):
        print(f"[ERROR] No se encontró el archivo de unidades de negocio: {csv_path}")
        print("Por favor verifica que el archivo exista en la carpeta 'data' de tu proyecto.")
        exit(1)
    df = pd.read_csv(csv_path, header=None, dtype=str)
    codigos = {}
    proceso = None
    planta_cols = None
    for i, row in df.iterrows():
        # Detectar fila de plantas
        if row[0] and str(row[0]).strip().upper() == 'PLANTAS':
            planta_cols = list(row)
            continue
        # Detectar fila de proceso principal
        if row[0] and row[1]:
            proceso = str(row[1]).strip()
            for idx, val in enumerate(row[2:], start=2):
                val_str = str(val).strip() if not pd.isna(val) else ''

    return None

# Generar variantes de nombre para el mes
def variantes_mes(mes):
    return [mes.lower(), mes.upper(), mes.capitalize()]

# Crear archivo CSV para el mes si no existe, copiando el formato de CSV_BASE
def crear_csv_mes(mes):
    base_name = "EDO RES ACUMULADO 2025-10 FINAL__"
    abs_csv_base = os.path.abspath(CSV_BASE)
    abs_csv_pages_dir = os.path.abspath(CSV_PAGES_DIR)
    # Si el archivo base no existe, generarlo usando split_xlsx_to_csv
    if not os.path.exists(abs_csv_base):
        print(f"[INFO] El archivo base {abs_csv_base} no existe. Generando con split_xlsx_to_csv...")
        if split_xlsx_to_csv:
            split_xlsx_to_csv(EXCEL_FILE=os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/EDO RES ACUMULADO 2025-10 FINAL.xlsx')),
                             OUTPUT_DIR=abs_csv_pages_dir)
        else:
            print("[ERROR] No se pudo importar split_xlsx_to_csv. No se puede generar el archivo base.")
            exit(1)
    for variante in variantes_mes(mes):
        csv_path = os.path.join(abs_csv_pages_dir, f"{base_name}{variante}.csv")
        if not os.path.exists(csv_path):
            # Copiar formato (solo encabezados y estructura)
            df_base = pd.read_csv(abs_csv_base, header=None)
            df_base.to_csv(csv_path, index=False, header=False)
            print(f"✔ Creado archivo para mes: {csv_path}")
        else:
            print(f"✔ Ya existe archivo para mes: {csv_path}")

# Plantilla para extraer y persistir datos del CSV manteniendo formato
def extraer_plantilla_csv_formato(input_path, output_path=None):
    resultado = []
    with open(input_path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile))
        num_cols = max(len(row) for row in reader if row)
        for idx, row in enumerate(reader):
            if not row:
                resultado.append([''] * num_cols)
                continue
            # Primeras 6 filas: conservar todas las columnas
            if idx < 6:
                nueva = row + [''] * (num_cols - len(row)) if len(row) < num_cols else row[:num_cols]
                resultado.append(nueva)
            else:
                # Solo la primera columna, el resto vacío
                col1 = row[0] if len(row) > 0 else ''
                nueva = [col1] + [''] * (num_cols - 1)
                resultado.append(nueva)
    if output_path:
        with open(output_path, 'w', newline='', encoding='utf-8') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerows(resultado)
    return resultado
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
            from data.splitXslsToCsv import split_xlsx_to_csv
            split_xlsx_to_csv()
        else:
            print(f"✔ Todos los archivos CSV del mes '{mes_detectado}' ya existen.")

    # --- NUEVA LÓGICA DE CRUCE Y AGRUPACIÓN ---
    import pandas as pd
    # Leer balanza y catálogo usando rutas absolutas
    # Primero, detectar la fila de encabezados correcta
    with open(INPUT_FILE, encoding='utf-8') as f:
        for i, line in enumerate(f):
            if 'Nº cuenta' in line or 'No cuenta' in line or 'Nro cuenta' in line:
                header_row = i
                print(f"[DEBUG] Encabezado encontrado en la fila: {header_row}")
                break
        else:
            raise Exception("No se encontró la fila de encabezados con 'Nº cuenta' en el archivo de balanza.")
    balanza = pd.read_csv(INPUT_FILE, header=header_row, dtype=str)
    print("[DEBUG] Columnas de balanza:", list(balanza.columns))
    catalogo = pd.read_csv(os.path.join(BASE_DIR, "data/CATALOGO CUENTAS GRALc.csv"), dtype=str)

    # Limpiar y normalizar columnas relevantes
    balanza = balanza.rename(columns=lambda x: x.strip() if isinstance(x, str) else x)
    catalogo = catalogo.rename(columns=lambda x: x.strip() if isinstance(x, str) else x)

    # Crear columna de código de cuenta normalizado en ambos
    def normaliza_codigo(cuenta):
        if pd.isna(cuenta):
            return None
        cuenta = str(cuenta).replace(" ", "").replace(".", "")
        return cuenta

    balanza["codigo_normalizado"] = balanza["Nº cuenta"].apply(normaliza_codigo)
    catalogo["codigo_normalizado"] = catalogo["Obj"].apply(normaliza_codigo)


    # Hacer merge para obtener la descripción del catálogo
    merged = pd.merge(
        balanza,
        catalogo[["codigo_normalizado", "Descripción de cuenta"]],
        on="codigo_normalizado",
        how="left"
    )
    print("[DEBUG] Columnas de merged:", list(merged.columns))

    # Agrupar por Cía y Descripción de cuenta, sumar columnas numéricas
    # Detectar columnas numéricas
    numeric_cols = []
    for col in merged.columns:
        try:
            merged[col].astype(float)
            numeric_cols.append(col)
        except:
            continue
    # Excluir columnas que no deben sumarse
    exclude = ["Nº cuenta", "N", "Descripción", "codigo_normalizado", "Descripción de cuenta", "Unidad de negocio", "Planta", "Centro de Costo", "ID cuenta", "Cía"]
    numeric_cols = [c for c in numeric_cols if c not in exclude]

    # Convertir columnas numéricas
    for col in numeric_cols:
        merged[col] = pd.to_numeric(merged[col], errors='coerce').fillna(0)

    # Agrupar y sumar usando 'Cía' en vez de 'Unidad de negocio'
    agrupado = merged.groupby([
        "Cía", "Descripción de cuenta"
    ], dropna=False)[numeric_cols].sum().reset_index()

    # Unir de nuevo para mantener todas las columnas originales
    final = pd.merge(
        merged.drop(columns=numeric_cols),
        agrupado,
        on=["Cía", "Descripción de cuenta"],
        how="left"
    )


    # Guardar resultado agrupado en archivo temporal
    output_temp = os.path.join(BASE_DIR, "data/output_balanza_agrupada_temp.csv")
    final.to_csv(output_temp, index=False)
    print(f"✔ Archivo agrupado generado: {output_temp}")

    # Usar el archivo plantilla correcto para el formato de salida
    plantilla_path = os.path.join(CSV_PAGES_DIR, "EDO RES ACUMULADO 2025-10 FINAL__OCTUBRE.csv")
    output_final = os.path.join(BASE_DIR, "data/output_balanza_agrupada_formato.csv")
    extraer_plantilla_csv_formato(plantilla_path, output_final)
    print(f"✔ Archivo con formato plantilla generado: {output_final}")

if __name__ == "__main__":
    main()
