#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte 2: Análisis cualitativo de Clusters
Lee el CSV generado en Parte1 (case_features_clusters.csv) y caracteriza cada cluster,
interpretando diferencias operativas. Muestra estadísticas por consola y exporta un
resumen a Data/cluster_analysis.txt.
"""
import os
import sys
import pandas as pd
from collections import Counter


def load_clustered(csv_path):
    print(f"[1/4] Cargando datos clusterizados: {csv_path}")
    if not os.path.isfile(csv_path):
        print(f"ERROR: No se encontró el archivo {csv_path}.")
        sys.exit(1)
    df = pd.read_csv(csv_path)
    print("    Datos cargados correctamente.")
    return df


def summarize_clusters(df):
    print("[2/4] Analizando clusters...")
    rows = []
    for cid, group in df.groupby('cluster'):
        dur_mean = group['duration_min'].mean()
        act_mean = group['num_activities'].mean()
        roles_mean = group['num_roles'].mean()
        start_mode = Counter(group['start_act']).most_common(1)[0][0]
        end_mode = Counter(group['end_act']).most_common(1)[0][0]
        print(f"  Cluster {cid}:")
        print(f"    Duración promedio: {dur_mean:.1f} min")
        print(f"    Actividades promedio: {act_mean:.1f}")
        print(f"    Roles promedio: {roles_mean:.1f}")
        print(f"    Inicio más común: {start_mode}")
        print(f"    Fin más común: {end_mode}")
        rows.append({
            'cluster': cid,
            'mean_duration': dur_mean,
            'mean_activities': act_mean,
            'mean_roles': roles_mean,
            'common_start_act': start_mode,
            'common_end_act': end_mode
        })
    print("    Resumen de clusters completado.")
    return pd.DataFrame(rows)


def save_summary(df_summary, output_path):
    print(f"[3/4] Guardando análisis en: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        for _, r in df_summary.iterrows():
            f.write(f"Cluster {int(r['cluster'])}:\n")
            f.write(f"  Duración promedio: {r['mean_duration']:.1f} min\n")
            f.write(f"  Actividades promedio: {r['mean_activities']:.1f}\n")
            f.write(f"  Roles promedio: {r['mean_roles']:.1f}\n")
            f.write(f"  Inicio más común: {r['common_start_act']}\n")
            f.write(f"  Fin más común: {r['common_end_act']}\n")
            f.write("\n")
    print("    Archivo de análisis guardado.")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'Data')
    csv_path = os.path.join(data_dir, 'case_features_clusters.csv')

    df = load_clustered(csv_path)
    summary_df = summarize_clusters(df)

    txt_out = os.path.join(data_dir, 'cluster_analysis.txt')
    save_summary(summary_df, txt_out)

    print("[4/4] Análisis cualitativo completado.")

if __name__ == '__main__':
    main()
