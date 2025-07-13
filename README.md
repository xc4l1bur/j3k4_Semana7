# j3k4_Semana7

# Proyecto de Análisis de Casos Operativos

Este proyecto implementa un flujo en **5 pasos** para:

1. Segmentar casos operativos.
2. Analizar cualitativamente los clústeres.
3. Entrenar modelos de regresión por clúster.
4. Evaluar los modelos (R² y RMSE).
5. Reflexionar y proponer mejoras operacionales.

Cada paso está encapsulado en un script `parteX.py` y orquestado con un **Makefile**.

---

## 1. Detalle de la actividad en 5 pasos

### Paso 1: Segmentación de Casos Operativos

* **Script:** `parte1.py`
* **Requiere:**

  * `Data/IDA703_data_semana_7.csv`
  * Paquetes: pandas, scikit‑learn, matplotlib, seaborn
* **Salida:**

  * `Data/case_features_clusters.csv`
  * `Data/clusters_duration_activities.png`

### Paso 2: Análisis cualitativo de clústeres

* **Script:** `parte2.py`
* **Requiere:** salida de Paso 1 (`case_features_clusters.csv`)
* **Salida:**

  * `Data/cluster_analysis.txt` (resumen de métricas e interpretación)

### Paso 3: Modelos de regresión por clúster

* **Script:** `parte3.py`
* **Requiere:** salida de Paso 1 (`case_features_clusters.csv`)
* **Salida:**

  * `Data/models/model_cluster_{cid}.pkl` (modelos serializados)
  * `Data/regression_summary.csv` (coeficientes)

### Paso 4: Evaluación de los modelos

* **Script:** `parte4.py`
* **Requiere:** modelos de Paso 3 y `case_features_clusters.csv`
* **Salida:**

  * `Data/model_evaluation.txt` (R², RMSE por clúster + mejor modelo)

### Paso 5: Reflexión y propuesta

* **Actividad manual:** basado en resultados anteriores, redactar conclusiones y recomendaciones.
* **No autoejecutable** (puede incluirse en la documentación final).

---

## Instalación

```bash
# Clonar el repositorio
# cd <directorio_del_proyecto>

# Crear y activar entorno, e instalar dependencias
make instalar
source .venv/bin/activate
```

**Requisitos:** Python 3.8+.

---

## Ejecución

Una vez instalado y con el entorno activo:

```bash
# Paso 1: Segmentación y clustering
make parte1

# Paso 2: Análisis cualitativo de clústeres
make parte2

# Paso 3: Entrenamiento de regresión
make parte3

# Paso 4: Evaluación de los modelos
make parte4
```

> Cada regla de `make` ejecuta automáticamente los prerequisitos necesarios.

---

## Estructura de carpetas

```
./
├── Makefile
├── requirements.txt
├── parte1.py
├── parte2.py
├── parte3.py
├── parte4.py
├── Data/
│   ├── IDA703_data_semana_7.csv
│   ├── case_features_clusters.csv
│   ├── clusters_duration_activities.png
│   ├── cluster_analysis.txt
│   ├── models/
│   │   ├── model_cluster_0.pkl
│   │   └── ...
│   ├── regression_summary.csv
│   └── model_evaluation.txt
└── README.md
```

---

Con esto tienes un flujo reproducible y documentado para procesar, analizar y evaluar tus casos operativos. ¡Éxito con tu proyecto!
