#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte 4: Evaluación del Modelo
Calcula R² y RMSE para cada modelo entrenado en Parte3.
Si faltan resultados de Parte3, los gatilla antes de calcular.
"""
import os
import sys
import subprocess
import pandas as pd
import pickle
import math
from sklearn.metrics import r2_score, mean_squared_error


def ensure_prerequisite(script, data_dir):
    # Verifica que existan los modelos entrenados y el CSV
    csv_path = os.path.join(data_dir, 'case_features_clusters.csv')
    models_dir = os.path.join(data_dir, 'models')
    if not os.path.isfile(csv_path) or not os.path.isdir(models_dir):
        print(f"=> Resultados de Parte3 no encontrados. Ejecutando {script}...")
        subprocess.run([sys.executable, script], check=True)


def load_data(data_dir):
    csv_path = os.path.join(data_dir, 'case_features_clusters.csv')
    print(f"[1/6] Cargando datos clusterizados: {csv_path}")
    df = pd.read_csv(csv_path)
    print("    Datos cargados correctamente.")
    return df


def evaluate_models(df, data_dir):
    print("[2/6] Evaluando modelos...")
    results = []
    models_dir = os.path.join(data_dir, 'models')
    for mdl_file in sorted(os.listdir(models_dir)):
        if not mdl_file.endswith('.pkl'):
            continue
        cid = int(mdl_file.split('_')[-1].split('.')[0])
        model_path = os.path.join(models_dir, mdl_file)
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        sub = df[df['cluster'] == cid]
        X = sub[['num_activities', 'num_roles', 'start_code', 'end_code']]
        y_true = sub['duration_min']
        y_pred = model.predict(X)
        r2 = r2_score(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = math.sqrt(mse)
        print(f"  Cluster {cid}: R² = {r2:.3f}, RMSE = {rmse:.3f} min")
        results.append({'cluster': cid, 'r2': r2, 'rmse': rmse})
    print("    Evaluación completada.")
    return pd.DataFrame(results)


def save_report(df_res, output_path):
    print(f"[5/6] Guardando informe en: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        best = df_res.loc[df_res['r2'].idxmax()]
        f.write("Evaluación de Modelos por Clúster\n")
        f.write("==============================\n")
        for _, row in df_res.iterrows():
            f.write(f"Cluster {int(row['cluster'])}: R²={row['r2']:.3f}, RMSE={row['rmse']:.3f} min\n")
        f.write("\n")
        f.write(f"Mayor precisión: Cluster {int(best['cluster'])} (R²={best['r2']:.3f})\n")
    print("    Informe guardado.")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'Data')

    # Paso preliminar: gatilla Parte3 si falta
    ensure_prerequisite('parte3.py', data_dir)

    df = load_data(data_dir)
    df_res = evaluate_models(df, data_dir)

    out_txt = os.path.join(data_dir, 'model_evaluation.txt')
    save_report(df_res, out_txt)

    print("[6/6] Evaluación completada. Revisa model_evaluation.txt en Data/.")

if __name__ == '__main__':
    main()
