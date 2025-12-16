import pandas as pd
import os
import re

def split_xlsx_to_csv(EXCEL_FILE="EDO RES ACUMULADO 2025-10 FINAL.xlsx", OUTPUT_DIR="csv_pages"):
    """
    Divide todas las hojas de un archivo Excel en archivos CSV individuales en OUTPUT_DIR.
    """
    base_name = os.path.splitext(os.path.basename(EXCEL_FILE))[0]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    xlsx = pd.ExcelFile(EXCEL_FILE)
    for sheet in xlsx.sheet_names:
        df = pd.read_excel(xlsx, sheet_name=sheet, dtype=str)
        safe_sheet = re.sub(r"[^\w\-]", "_", sheet)
        csv_name = f"{base_name}__{safe_sheet}.csv"
        output_path = os.path.join(OUTPUT_DIR, csv_name)
        df.to_csv(output_path, index=False)
        print(f"✔ Generado: {output_path}")

# Permite ejecución directa como script
if __name__ == "__main__":
    split_xlsx_to_csv()
