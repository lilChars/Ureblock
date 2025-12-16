# src/main.py
from reader import read_file
from processor import process_data
from writer import write_file

INPUT_FILE = "data/input/archivo1.csv"
OUTPUT_FILE = "data/output/resultado.xlsx"

def main():
    df = read_file(INPUT_FILE)
    result = process_data(df)
    write_file(result, OUTPUT_FILE)
    print("✔ Proceso completado")

if __name__ == "__main__":
    main()
