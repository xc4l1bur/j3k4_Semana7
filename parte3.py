#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte 3: Modelo de Regresión por Clúster
Para cada clúster entrenaremos un modelo de Regresión Lineal
y guardaremos resultados y modelos en Data/.
"""
import os
import sys
import subprocess
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression


def ensure_prerequisite(script, data_file):
    if not os.path.isfile(data_file):
        print(f"No se encontró {data_file}. Ejecutando {script}...")
        subprocess.run([sys.executable, script], check=True)


def load_clustered(csv_path):
    print(f"[1/5] Cargando datos clusterizados: {csv_path}")
    if not os.path.isfile(csv_path):
        print(f"ERROR: Archivo no encontrado: {csv_path}")
        sys.exit(1)
    df = pd.read_csv(csv_path)
    print("    Datos cargados correctamente.")
    return df


def train_regression_models(df):
    print("[2/5] Entrenando modelos de Regresión Lineal por clúster...")
    models = {}
    summaries = []
    # Variables predictoras
    X_cols = ['num_activities', 'num_roles', 'start_code', 'end_code']
    for cid, group in df.groupby('cluster'):
        print(f"  Cluster {cid}: n={len(group)} casos")
        X = group[X_cols]
        y = group['duration_min']
        model = LinearRegression()
        model.fit(X, y)
        models[cid] = model
        # Imprimir coeficientes
        print(f"    Intercept: {model.intercept_:.3f}")
        for feat, coef in zip(X_cols, model.coef_):
            print(f"    Coeficiente {feat}: {coef:.3f}")
        summaries.append({
            'cluster': cid,
            'intercept': model.intercept_,
            **{f'coef_{feat}': coef for feat, coef in zip(X_cols, model.coef_)}
        })
    print("    Modelos entrenados.")
    return models, pd.DataFrame(summaries)


def save_models(models, output_dir):
    print(f"[3/5] Guardando modelos en: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    for cid, model in models.items():
        path = os.path.join(output_dir, f'model_cluster_{cid}.pkl')
        with open(path, 'wb') as f:
            pickle.dump(model, f)
    print("    Modelos guardados.")


def save_summary(df_summary, output_path):
    print(f"[4/5] Guardando resumen de coeficientes en: {output_path}")
    df_summary.to_csv(output_path, index=False)
    print("    Resumen guardado.")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'Data')

    # Asegurar que parte1 ha corrido
    csv_features = os.path.join(data_dir, 'case_features_clusters.csv')
    ensure_prerequisite('parte1.py', csv_features)

    # Cargar datos
    df = load_clustered(csv_features)

    # Entrenar modelos
    models, summary_df = train_regression_models(df)

    # Guardar modelos y resumen
    models_dir = os.path.join(data_dir, 'models')
    save_models(models, models_dir)

    summary_csv = os.path.join(data_dir, 'regression_summary.csv')
    save_summary(summary_df, summary_csv)

    print("[5/5] Parte3 completada. Modelos y resumen disponibles en carpeta Data.")


if __name__ == '__main__':
    main()
