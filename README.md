Este proyecto es un MVP en Python que lee archivos CSV y XLSX, procesa los datos (sumas y catalogación) y genera un nuevo archivo de salida en Excel o CSV.

Soporta archivos grandes (≈15,000 filas) sin problemas de rendimiento.

🛠 Requisitos

Python 3.10 o superior

pip

Verificar instalación:

python --version
pip --version

📦 Instalación
1️⃣ Clonar el repositorio
git clone https://github.com/tuusuario/excel-mvp.git
cd excel-mvp

2️⃣ Crear entorno virtual
python -m venv venv

Activar entorno:

Windows

venv\Scripts\activate

Mac / Linux

source venv/bin/activate

3️⃣ Instalar dependencias desde req
pip install -r req

📁 Estructura del proyecto
excel-mvp/
│
├─ data/
│ ├─ input/
│ │ ├─ archivo.csv
│ │ └─ archivo.xlsx
│ │
│ └─ output/
│ └─ resultado.xlsx
│
├─ src/
│ ├─ main.py
│ ├─ reader.py
│ ├─ processor.py
│ └─ writer.py
│
├─ req
├─ README.md
└─ .gitignore

▶️ Uso
1️⃣ Colocar archivos de entrada

Copia los archivos CSV o XLSX dentro de:

data/input/

2️⃣ Ejecutar el proceso
python src/main.py

3️⃣ Resultado

El archivo procesado se generará en:

data/output/resultado.xlsx

⚙️ Lógica de procesamiento

Lectura automática de CSV o XLSX

Limpieza básica de datos

Agrupación y suma de valores

Escritura del resultado en archivo nuevo

La lógica principal se encuentra en src/processor.py

⚡ Rendimiento
Filas por archivo Tiempo aproximado
5,000 < 0.05 s
15,000 < 0.1 s
100,000 ~0.5 s
