#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte 1: Segmentación de Casos Operativos
Lee el CSV de eventos desde la carpeta Data, extrae características por caso y aplica clustering.
Muestra el progreso por consola, guarda resultados CSV y gráfico PNG en Data, y muestra el gráfico.
"""
import os
import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


def load_event_log(csv_path):
    print(f"[1/5] Cargando datos de: {csv_path}")
    if not os.path.isfile(csv_path):
        print(f"ERROR: El archivo {csv_path} no existe.")
        sys.exit(1)
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    print("    Datos cargados correctamente.")
    return df


def extract_case_features(df):
    print("[2/5] Extrayendo características por caso...")
    df_sorted = df.sort_values(['case_id', 'timestamp'])
    agg = df_sorted.groupby('case_id').agg(
        duration_min = ('timestamp', lambda x: (x.max() - x.min()).total_seconds() / 60),
        num_activities = ('activity', 'count'),
        num_roles      = ('role', lambda x: x.nunique()),
        start_act      = ('activity', lambda x: x.iloc[0]),
        end_act        = ('activity', lambda x: x.iloc[-1])
    ).reset_index()
    le = LabelEncoder()
    agg['start_code'] = le.fit_transform(agg['start_act'])
    agg['end_code']   = le.fit_transform(agg['end_act'])
    print("    Características extraídas.")
    return agg


def apply_clustering(agg, n_clusters=3):
    print(f"[3/5] Aplicando KMeans con n_clusters={n_clusters}...")
    model = KMeans(n_clusters=n_clusters, random_state=42)
    features = agg[['duration_min', 'num_activities', 'num_roles', 'start_code', 'end_code']]
    agg['cluster'] = model.fit_predict(features)
    print("    Clustering completado.")
    return agg, model


def plot_clusters(agg, output_path):
    print(f"[4/5] Generando gráfico de clusters y guardando como: {output_path}")
    sns.set(style='whitegrid')
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=agg,
        x='duration_min',
        y='num_activities',
        hue='cluster',
        palette='deep',
        s=100
    )
    plt.title('Clusters de Casos: Duración vs Número de Actividades')
    plt.xlabel('Duración (min)')
    plt.ylabel('Número de Actividades')
    plt.legend(title='Cluster')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()
    print("    Gráfico mostrado y guardado.")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'Data')
    os.makedirs(data_dir, exist_ok=True)

    csv_path = os.path.join(data_dir, 'IDA703_data_semana_7.csv')
    df = load_event_log(csv_path)

    agg = extract_case_features(df)

    agg_clustered, _ = apply_clustering(agg.copy(), n_clusters=3)

    output_csv = os.path.join(data_dir, 'case_features_clusters.csv')
    print(f"[5/5] Guardando resultados de clustering en: {output_csv}")
    agg_clustered.to_csv(output_csv, index=False)
    print("    Archivo CSV generado.")

    plot_path = os.path.join(data_dir, 'clusters_duration_activities.png')
    plot_clusters(agg_clustered, plot_path)

    print("Ejecución completada. Archivos generados en carpeta Data.")


if __name__ == '__main__':
    main()