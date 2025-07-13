# Makefile: Orquesta ejecución de Parte1, Parte2 y Parte3

# Objetivo por defecto: mostrar ayuda
.DEFAULT_GOAL := help

.PHONY: help instalar limpiar parte1 parte2 parte3

help:
	@echo "Opciones disponibles:"
	@echo "  make            -> Muestra este mensaje"
	@echo "  make instalar   -> Crea entorno virtual e instala requerimientos"
	@echo "  make limpiar    -> Elimina .venv y Data para comenzar de cero"
	@echo "  make parte1     -> Ejecuta parte1.py usando CSV en Data/"
	@echo "  make parte2     -> Ejecuta parte2.py después de parte1"
	@echo "  make parte3     -> Ejecuta parte3.py (solo requiere parte1)"

instalar:
	python3 -m venv .venv
	@echo "Entorno virtual creado en .venv"
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@echo "Dependencias instaladas"
	@echo "Para activar el entorno: source .venv/bin/activate"

limpiar:
	rm -rf .venv Data
	@echo "Entorno y carpeta Data eliminados"

parte1:
	@echo "Validando existencia de Data/IDA703_data_semana_7.csv"
	@test -f Data/IDA703_data_semana_7.csv \
		|| { echo "ERROR: Data/IDA703_data_semana_7.csv no encontrada"; exit 1; }
	@echo "Ejecutando parte1.py"
	.venv/bin/python parte1.py

parte2: parte1
	@echo "Validando existencia de Data/case_features_clusters.csv"
	@test -f Data/case_features_clusters.csv \
		|| { echo "ERROR: Data/case_features_clusters.csv no encontrada. Ejecuta make parte1 primero."; exit 1; }
	@echo "Ejecutando parte2.py"
	.venv/bin/python parte2.py

parte3: parte1
	@echo "Validando existencia de Data/case_features_clusters.csv"
	@test -f Data/case_features_clusters.csv \
		|| { echo "ERROR: Data/case_features_clusters.csv no encontrada. Ejecuta make parte1 primero."; exit 1; }
	@echo "Ejecutando parte3.py"
	.venv/bin/python parte3.py

parte4: parte3
	@echo "Ejecutando parte4.py (evaluación de modelos)"
	.venv/bin/python parte4.py

