#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
20_plot_caracteristicas_dataset.py
----------------------------------
Generador de figuras estadísticas para las características del corpus generado (Apartado 5.3):
Diseñado con los datos reparados de 'data/generator_input.json' y 'data/generator_output.json'.

Figuras generadas:
1. Figura 3: Prevalencia de cada código CIF por historia clínica (N = 114).
2. Figura 4: Frecuencia relativa sobre el total de códigos (n = 465 menciones).
3. Figura 5: Frecuencia relativa sobre el total excluyendo b280 (n = 360 menciones).
4. Figura 2-en-1 Horizontal (Panel A: Frecuencia Total, Panel B: Frecuencia sin b280).
5. Figura 3-en-1 Horizontal (Panel A: Prevalencia, Panel B: Frecuencia Total, Panel C: Frecuencia sin b280).
6. Figura de Distribución por Componente CIF (b: Funciones, d: Actividades, e: Factores Ambientales).

Formatos de exportación:
- PNG de alta resolución (300 DPI, optimizado para documentos e informes)
- PDF vectorial (calidad de imprenta / LaTeX / editorial)
- SVG vectorial (para visualización web y dashboard interactivo)
"""

import os
import sys
import json
from pathlib import Path
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = BASE_DIR / 'data' / 'generator_input.json'
OUTPUT_FILE = BASE_DIR / 'data' / 'generator_output.json'
FIGURAS_DIR = BASE_DIR / 'results' / 'TFL' / 'figuras'

COMPONENT_MAP = {
    'b': {'name': 'Funciones corporales', 'color': '#2563EB', 'light': '#93C5FD', 'edge': '#1E40AF'},
    'd': {'name': 'Actividades y participación', 'color': '#0D9488', 'light': '#5EEAD4', 'edge': '#0F766E'},
    'e': {'name': 'Factores ambientales', 'color': '#D97706', 'light': '#FCD34D', 'edge': '#B45309'},
    's': {'name': 'Estructuras corporales', 'color': '#7C3AED', 'light': '#C4B5FD', 'edge': '#6D28D9'}
}

COLOR_B280 = '#93C5FD'        # Azul cielo distintivo acorde a la leyenda del TFM
COLOR_B280_EDGE = '#1D4ED8'   # Borde azul cobalto
COLOR_DEFAULT = '#3B82F6'     # Azul clínico estándar
COLOR_DEFAULT_EDGE = '#1E3A8A'


def setup_plot_style():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans', 'Times New Roman'],
        'axes.edgecolor': '#334155',
        'axes.linewidth': 1.1,
        'axes.labelcolor': '#0F172A',
        'axes.titlecolor': '#0F172A',
        'xtick.color': '#0F172A',
        'ytick.color': '#0F172A',
        'grid.color': '#E2E8F0',
        'grid.linestyle': '--',
        'grid.alpha': 0.75,
        'figure.facecolor': '#FFFFFF',
        'axes.facecolor': '#FFFFFF'
    })


def load_dataset_stats():
    if not OUTPUT_FILE.exists():
        raise FileNotFoundError(f'No se encontró el archivo de datos: {OUTPUT_FILE}')

    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    code_names = {}
    if INPUT_FILE.exists():
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            inp_data = json.load(f)
        for item in inp_data:
            for c, name in zip(item.get('icf_codes', []), item.get('icf_name', [])):
                code_names[c] = name

    for item in data:
        for c, name in zip(item.get('icf_codes', []), item.get('icf_name', [])):
            if c not in code_names:
                code_names[c] = name

    n_cases = len(data)
    all_codes = []
    case_code_sets = []

    for item in data:
        codes = item.get('icf_codes', [])
        all_codes.extend(codes)
        case_code_sets.append(set(codes))

    total_codes = len(all_codes)
    counts = Counter(all_codes)

    # 1. Prevalencia (% de historias clínicas N=114)
    prev_data = []
    for c, count in counts.items():
        n_prev = sum(1 for s in case_code_sets if c in s)
        pct_prev = (n_prev / n_cases) * 100
        comp = c[0]
        name = code_names.get(c, c)
        prev_data.append({
            'code': c,
            'name': name,
            'component': comp,
            'component_name': COMPONENT_MAP.get(comp, {}).get('name', comp),
            'n_cases': n_prev,
            'pct': pct_prev
        })
    df_prev = pd.DataFrame(prev_data).sort_values('pct', ascending=False).reset_index(drop=True)

    # 2. Frecuencia relativa total (% sobre n=465 menciones)
    freq_data = []
    for c, count in counts.items():
        pct_freq = (count / total_codes) * 100
        comp = c[0]
        name = code_names.get(c, c)
        freq_data.append({
            'code': c,
            'name': name,
            'component': comp,
            'component_name': COMPONENT_MAP.get(comp, {}).get('name', comp),
            'count': count,
            'pct': pct_freq
        })
    df_freq = pd.DataFrame(freq_data).sort_values('pct', ascending=False).reset_index(drop=True)

    # 3. Frecuencia relativa sin b280 (% sobre n=360 menciones restantes)
    no_b280_codes = [c for c in all_codes if c != 'b280']
    total_no_b280 = len(no_b280_codes)
    no_b280_counts = Counter(no_b280_codes)

    freq_no_b280_data = []
    for c, count in no_b280_counts.items():
        pct_no_b280 = (count / total_no_b280) * 100
        comp = c[0]
        name = code_names.get(c, c)
        freq_no_b280_data.append({
            'code': c,
            'name': name,
            'component': comp,
            'component_name': COMPONENT_MAP.get(comp, {}).get('name', comp),
            'count': count,
            'pct': pct_no_b280
        })
    df_freq_no_b280 = pd.DataFrame(freq_no_b280_data).sort_values('pct', ascending=False).reset_index(drop=True)

    return df_prev, df_freq, df_freq_no_b280, n_cases, total_codes, total_no_b280


def save_multiformat(fig, base_name: str):
    FIGURAS_DIR.mkdir(parents=True, exist_ok=True)
    p_png = FIGURAS_DIR / f'{base_name}.png'
    p_pdf = FIGURAS_DIR / f'{base_name}.pdf'
    p_svg = FIGURAS_DIR / f'{base_name}.svg'

    fig.savefig(p_png, dpi=300, bbox_inches='tight')
    fig.savefig(p_pdf, format='pdf', bbox_inches='tight')
    fig.savefig(p_svg, format='svg', bbox_inches='tight')
    print(f'  [OK] Guardado: {p_png.name} (.png, .pdf, .svg)')


def plot_figura3_prevalencia(df_prev, n_cases):
    fig, ax = plt.subplots(figsize=(13.0, 5.5), dpi=300)
    ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

    colors = [COLOR_B280 if row['code'] == 'b280' else COLOR_DEFAULT for _, row in df_prev.iterrows()]
    edge_colors = [COLOR_B280_EDGE if row['code'] == 'b280' else COLOR_DEFAULT_EDGE for _, row in df_prev.iterrows()]

    bars = ax.bar(
        df_prev['code'],
        df_prev['pct'],
        color=colors,
        edgecolor=edge_colors,
        linewidth=1.2,
        zorder=3
    )

    ax.set_ylabel('Prevalencia en historias clínicas (%)', fontsize=13.0, fontweight='bold', labelpad=10)
    ax.set_xlabel('Código CIF', fontsize=13.0, fontweight='bold', labelpad=10)
    ax.set_ylim(0, 110)
    ax.set_xticks(range(len(df_prev)))
    ax.set_xticklabels(df_prev['code'], rotation=90, ha='center', fontsize=11.0, fontweight='bold')
    ax.tick_params(axis='y', labelsize=11.0)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for bar, pct, n_p in zip(bars, df_prev['pct'], df_prev['n_cases']):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 2.0,
            f'{pct:.1f}%',
            ha='center',
            va='bottom',
            rotation=90,
            fontsize=9.5,
            fontweight='bold',
            color='#1E293B',
            zorder=4
        )

    patch_b280 = mpatches.Patch(facecolor=COLOR_B280, edgecolor=COLOR_B280_EDGE, linewidth=1.1, label='Clase prevalente (b280: 92.1%)')
    patch_other = mpatches.Patch(facecolor=COLOR_DEFAULT, edgecolor=COLOR_DEFAULT_EDGE, linewidth=1.1, label='Otras categorías CIF (7.9% - 23.7%)')
    ax.legend(handles=[patch_b280, patch_other], loc='upper right', frameon=True, framealpha=0.95, edgecolor='#CBD5E1', fontsize=10.5)

    plt.tight_layout()

    save_multiformat(fig, 'figura3_prevalencia_casos_clinicos')
    save_multiformat(fig, '01_prevalencia_casos_cif')
    save_multiformat(fig, 'figura_prevalencia_casos_clinicos')
    plt.close(fig)


def plot_figura4_frecuencia_total(df_freq, total_codes):
    fig, ax = plt.subplots(figsize=(13.0, 5.5), dpi=300)
    ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

    colors = [COLOR_B280 if row['code'] == 'b280' else COLOR_DEFAULT for _, row in df_freq.iterrows()]
    edge_colors = [COLOR_B280_EDGE if row['code'] == 'b280' else COLOR_DEFAULT_EDGE for _, row in df_freq.iterrows()]

    bars = ax.bar(
        df_freq['code'],
        df_freq['pct'],
        color=colors,
        edgecolor=edge_colors,
        linewidth=1.2,
        zorder=3
    )

    ax.set_ylabel('Frecuencia relativa (%)', fontsize=13.0, fontweight='bold', labelpad=10)
    ax.set_xlabel('Código CIF', fontsize=13.0, fontweight='bold', labelpad=10)
    ax.set_ylim(0, 27.5)
    ax.set_xticks(range(len(df_freq)))
    ax.set_xticklabels(df_freq['code'], rotation=90, ha='center', fontsize=11.0, fontweight='bold')
    ax.tick_params(axis='y', labelsize=11.0)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for bar, pct, count in zip(bars, df_freq['pct'], df_freq['count']):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.5,
            f'{pct:.1f}%',
            ha='center',
            va='bottom',
            rotation=90,
            fontsize=9.5,
            fontweight='bold',
            color='#1E293B',
            zorder=4
        )

    patch_b280 = mpatches.Patch(facecolor=COLOR_B280, edgecolor=COLOR_B280_EDGE, linewidth=1.1, label=f'Clase prevalente b280 (n = 105, 22.6%)')
    patch_other = mpatches.Patch(facecolor=COLOR_DEFAULT, edgecolor=COLOR_DEFAULT_EDGE, linewidth=1.1, label=f'Otras categorías CIF (n = 360, 77.4%)')
    ax.legend(handles=[patch_b280, patch_other], loc='upper right', frameon=True, framealpha=0.95, edgecolor='#CBD5E1', fontsize=10.5)

    plt.tight_layout()

    save_multiformat(fig, 'figura4_frecuencia_relativa_total')
    save_multiformat(fig, '02_frecuencia_relativa_total_cif')
    plt.close(fig)


def plot_figura5_frecuencia_sin_b280(df_freq_no_b280, total_no_b280):
    fig, ax = plt.subplots(figsize=(13.0, 5.5), dpi=300)
    ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

    bars = ax.bar(
        df_freq_no_b280['code'],
        df_freq_no_b280['pct'],
        color=COLOR_DEFAULT,
        edgecolor=COLOR_DEFAULT_EDGE,
        linewidth=1.2,
        zorder=3
    )

    ax.set_ylabel('Frecuencia relativa (%)', fontsize=13.0, fontweight='bold', labelpad=10)
    ax.set_xlabel('Código CIF', fontsize=13.0, fontweight='bold', labelpad=10)
    ax.set_ylim(0, 9.2)
    ax.set_xticks(range(len(df_freq_no_b280)))
    ax.set_xticklabels(df_freq_no_b280['code'], rotation=90, ha='center', fontsize=11.0, fontweight='bold')
    ax.tick_params(axis='y', labelsize=11.0)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for bar, pct, count in zip(bars, df_freq_no_b280['pct'], df_freq_no_b280['count']):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.18,
            f'{pct:.1f}%',
            ha='center',
            va='bottom',
            rotation=90,
            fontsize=9.5,
            fontweight='bold',
            color='#1E293B',
            zorder=4
        )

    info_box = dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.0)
    ax.text(0.98, 0.94, f'Total menciones no-dolor: n = {total_no_b280}\nCategorías únicas: 23 códigos',
            transform=ax.transAxes, ha='right', va='top', fontsize=10.5, fontweight='medium', color='#334155', bbox=info_box)

    plt.tight_layout()

    save_multiformat(fig, 'figura5_frecuencia_relativa_sin_b280')
    save_multiformat(fig, '03_frecuencia_relativa_sin_b280_cif')
    plt.close(fig)


def plot_figura_2en1_horizontal(df_freq, df_freq_no_b280, total_codes, total_no_b280):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17.0, 5.6), dpi=300)

    # PANEL A
    ax1.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
    colors1 = [COLOR_B280 if row['code'] == 'b280' else COLOR_DEFAULT for _, row in df_freq.iterrows()]
    edge_colors1 = [COLOR_B280_EDGE if row['code'] == 'b280' else COLOR_DEFAULT_EDGE for _, row in df_freq.iterrows()]
    bars1 = ax1.bar(df_freq['code'], df_freq['pct'], color=colors1, edgecolor=edge_colors1, linewidth=1.1, zorder=3)

    ax1.set_ylabel('Frecuencia relativa (%)', fontsize=12.5, fontweight='bold', labelpad=10)
    ax1.set_xlabel('Código CIF', fontsize=12.5, fontweight='bold', labelpad=10)
    ax1.set_ylim(0, 27.5)
    ax1.set_xticks(range(len(df_freq)))
    ax1.set_xticklabels(df_freq['code'], rotation=90, ha='center', fontsize=10.2, fontweight='bold')
    ax1.tick_params(axis='y', labelsize=10.5)
    ax1.set_title(f'A. Frecuencia relativa total (n = {total_codes} códigos)', fontsize=13.5, fontweight='bold', color='#0F172A', pad=12, loc='left')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    for bar, pct in zip(bars1, df_freq['pct']):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2.0, height + 0.5, f'{pct:.1f}%',
                 ha='center', va='bottom', rotation=90, fontsize=8.8, fontweight='bold', color='#1E293B', zorder=4)

    # PANEL B
    ax2.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
    bars2 = ax2.bar(df_freq_no_b280['code'], df_freq_no_b280['pct'], color=COLOR_DEFAULT, edgecolor=COLOR_DEFAULT_EDGE, linewidth=1.1, zorder=3)

    ax2.set_ylabel('Frecuencia relativa (%)', fontsize=12.5, fontweight='bold', labelpad=10)
    ax2.set_xlabel('Código CIF', fontsize=12.5, fontweight='bold', labelpad=10)
    ax2.set_ylim(0, 9.2)
    ax2.set_xticks(range(len(df_freq_no_b280)))
    ax2.set_xticklabels(df_freq_no_b280['code'], rotation=90, ha='center', fontsize=10.2, fontweight='bold')
    ax2.tick_params(axis='y', labelsize=10.5)
    ax2.set_title(f'B. Frecuencia relativa sin b280 (n = {total_no_b280} códigos)', fontsize=13.5, fontweight='bold', color='#0F172A', pad=12, loc='left')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    for bar, pct in zip(bars2, df_freq_no_b280['pct']):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2.0, height + 0.18, f'{pct:.1f}%',
                 ha='center', va='bottom', rotation=90, fontsize=8.8, fontweight='bold', color='#1E293B', zorder=4)

    plt.tight_layout()
    save_multiformat(fig, 'figura_frecuencia_relativa_2en1_horizontal')
    plt.close(fig)


def plot_figura_3en1_horizontal(df_prev, df_freq, df_freq_no_b280, n_cases, total_codes, total_no_b280):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(23.0, 5.8), dpi=300)

    # PANEL A: Prevalencia
    ax1.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
    c1 = [COLOR_B280 if r['code'] == 'b280' else COLOR_DEFAULT for _, r in df_prev.iterrows()]
    e1 = [COLOR_B280_EDGE if r['code'] == 'b280' else COLOR_DEFAULT_EDGE for _, r in df_prev.iterrows()]
    b1 = ax1.bar(df_prev['code'], df_prev['pct'], color=c1, edgecolor=e1, linewidth=1.1, zorder=3)
    ax1.set_ylabel('Prevalencia en casos (%)', fontsize=11.5, fontweight='bold')
    ax1.set_xlabel('Código CIF', fontsize=11.5, fontweight='bold')
    ax1.set_ylim(0, 110)
    ax1.set_xticks(range(len(df_prev)))
    ax1.set_xticklabels(df_prev['code'], rotation=90, ha='center', fontsize=9.5, fontweight='bold')
    ax1.set_title(f'A. Prevalencia por caso (N = {n_cases})', fontsize=12.5, fontweight='bold', loc='left')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    for b, pct in zip(b1, df_prev['pct']):
        ax1.text(b.get_x() + b.get_width() / 2.0, b.get_height() + 2.0, f'{pct:.1f}%',
                 ha='center', va='bottom', rotation=90, fontsize=8.0, fontweight='bold', color='#1E293B', zorder=4)

    # PANEL B: Frecuencia Total
    ax2.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
    c2 = [COLOR_B280 if r['code'] == 'b280' else COLOR_DEFAULT for _, r in df_freq.iterrows()]
    e2 = [COLOR_B280_EDGE if r['code'] == 'b280' else COLOR_DEFAULT_EDGE for _, r in df_freq.iterrows()]
    b2 = ax2.bar(df_freq['code'], df_freq['pct'], color=c2, edgecolor=e2, linewidth=1.1, zorder=3)
    ax2.set_ylabel('Frecuencia relativa (%)', fontsize=11.5, fontweight='bold')
    ax2.set_xlabel('Código CIF', fontsize=11.5, fontweight='bold')
    ax2.set_ylim(0, 27.5)
    ax2.set_xticks(range(len(df_freq)))
    ax2.set_xticklabels(df_freq['code'], rotation=90, ha='center', fontsize=9.5, fontweight='bold')
    ax2.set_title(f'B. Frecuencia total (n = {total_codes})', fontsize=12.5, fontweight='bold', loc='left')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    for b, pct in zip(b2, df_freq['pct']):
        ax2.text(b.get_x() + b.get_width() / 2.0, b.get_height() + 0.5, f'{pct:.1f}%',
                 ha='center', va='bottom', rotation=90, fontsize=8.0, fontweight='bold', color='#1E293B', zorder=4)

    # PANEL C: Frecuencia sin b280
    ax3.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
    b3 = ax3.bar(df_freq_no_b280['code'], df_freq_no_b280['pct'], color=COLOR_DEFAULT, edgecolor=COLOR_DEFAULT_EDGE, linewidth=1.1, zorder=3)
    ax3.set_ylabel('Frecuencia relativa (%)', fontsize=11.5, fontweight='bold')
    ax3.set_xlabel('Código CIF', fontsize=11.5, fontweight='bold')
    ax3.set_ylim(0, 9.2)
    ax3.set_xticks(range(len(df_freq_no_b280)))
    ax3.set_xticklabels(df_freq_no_b280['code'], rotation=90, ha='center', fontsize=9.5, fontweight='bold')
    ax3.set_title(f'C. Frecuencia sin b280 (n = {total_no_b280})', fontsize=12.5, fontweight='bold', loc='left')
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    for b, pct in zip(b3, df_freq_no_b280['pct']):
        ax3.text(b.get_x() + b.get_width() / 2.0, b.get_height() + 0.18, f'{pct:.1f}%',
                 ha='center', va='bottom', rotation=90, fontsize=8.0, fontweight='bold', color='#1E293B', zorder=4)

    plt.tight_layout()
    save_multiformat(fig, 'figura_distribucion_codigos_3en1_horizontal')
    plt.close(fig)


def plot_figura_componentes_cif(df_prev, df_freq, df_freq_no_b280):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18.0, 5.8), dpi=300)

    # Panel 1: Prevalencia con color por componente
    ax1.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
    c_prev = [COMPONENT_MAP.get(r['component'], {}).get('color', '#64748B') for _, r in df_prev.iterrows()]
    e_prev = [COMPONENT_MAP.get(r['component'], {}).get('edge', '#334155') for _, r in df_prev.iterrows()]
    bars1 = ax1.bar(df_prev['code'], df_prev['pct'], color=c_prev, edgecolor=e_prev, linewidth=1.1, zorder=3)

    ax1.set_ylabel('Prevalencia en historias clínicas (%)', fontsize=12.5, fontweight='bold', labelpad=10)
    ax1.set_xlabel('Código CIF', fontsize=12.5, fontweight='bold', labelpad=10)
    ax1.set_ylim(0, 110)
    ax1.set_xticks(range(len(df_prev)))
    ax1.set_xticklabels(df_prev['code'], rotation=90, ha='center', fontsize=10.2, fontweight='bold')
    ax1.tick_params(axis='y', labelsize=10.5)
    ax1.set_title('A. Prevalencia por historia clínica según Componente CIF', fontsize=13.0, fontweight='bold', loc='left')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    for bar, pct in zip(bars1, df_prev['pct']):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2.0, height + 2.0, f'{pct:.1f}%',
                 ha='center', va='bottom', rotation=90, fontsize=8.8, fontweight='bold', color='#1E293B', zorder=4)

    # Panel 2: Frecuencia sin b280 con color por componente
    ax2.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
    c_no_b = [COMPONENT_MAP.get(r['component'], {}).get('color', '#64748B') for _, r in df_freq_no_b280.iterrows()]
    e_no_b = [COMPONENT_MAP.get(r['component'], {}).get('edge', '#334155') for _, r in df_freq_no_b280.iterrows()]
    bars2 = ax2.bar(df_freq_no_b280['code'], df_freq_no_b280['pct'], color=c_no_b, edgecolor=e_no_b, linewidth=1.1, zorder=3)

    ax2.set_ylabel('Frecuencia relativa (%)', fontsize=12.5, fontweight='bold', labelpad=10)
    ax2.set_xlabel('Código CIF', fontsize=12.5, fontweight='bold', labelpad=10)
    ax2.set_ylim(0, 9.2)
    ax2.set_xticks(range(len(df_freq_no_b280)))
    ax2.set_xticklabels(df_freq_no_b280['code'], rotation=90, ha='center', fontsize=10.2, fontweight='bold')
    ax2.tick_params(axis='y', labelsize=10.5)
    ax2.set_title('B. Frecuencia relativa sin b280 según Componente CIF', fontsize=13.0, fontweight='bold', loc='left')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    for bar, pct in zip(bars2, df_freq_no_b280['pct']):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2.0, height + 0.18, f'{pct:.1f}%',
                 ha='center', va='bottom', rotation=90, fontsize=8.8, fontweight='bold', color='#1E293B', zorder=4)

    legend_patches = [
        mpatches.Patch(facecolor=COMPONENT_MAP['b']['color'], edgecolor=COMPONENT_MAP['b']['edge'], label='b: Funciones corporales'),
        mpatches.Patch(facecolor=COMPONENT_MAP['d']['color'], edgecolor=COMPONENT_MAP['d']['edge'], label='d: Actividades y participación'),
        mpatches.Patch(facecolor=COMPONENT_MAP['e']['color'], edgecolor=COMPONENT_MAP['e']['edge'], label='e: Factores ambientales')
    ]
    ax1.legend(handles=legend_patches, loc='upper right', frameon=True, framealpha=0.95, edgecolor='#CBD5E1', fontsize=10.0)
    ax2.legend(handles=legend_patches, loc='upper right', frameon=True, framealpha=0.95, edgecolor='#CBD5E1', fontsize=10.0)

    plt.tight_layout()
    save_multiformat(fig, 'figura_distribucion_codigos_por_componente')
    plt.close(fig)


def main():
    print('=' * 80)
    print(' 📊 GENERACIÓN DE FIGURAS DE PREVALENCIA Y FRECUENCIA CIF (APARTADO 5.3)')
    print('=' * 80)
    print(f' 📂 Datos de entrada : {INPUT_FILE}')
    print(f' 📂 Datos generados  : {OUTPUT_FILE}')
    print(f' 📁 Directorio salida: {FIGURAS_DIR}')
    print('-' * 80)

    setup_plot_style()
    df_prev, df_freq, df_freq_no_b280, n_cases, total_codes, total_no_b280 = load_dataset_stats()

    print(f' • Muestra de historias clínicas  : N = {n_cases}')
    print(f' • Menciones totales de códigos   : n = {total_codes}')
    print(f' • Menciones totales sin b280     : n = {total_no_b280}')
    print(f' • Categorías únicas identificadas: {len(df_prev)} códigos CIF')
    print('-' * 80)

    print('\n🎨 [1/6] Generando Figura 3: Prevalencia por historia clínica (N = 114)...')
    plot_figura3_prevalencia(df_prev, n_cases)

    print('\n🎨 [2/6] Generando Figura 4: Frecuencia relativa total (n = 465)...')
    plot_figura4_frecuencia_total(df_freq, total_codes)

    print('\n🎨 [3/6] Generando Figura 5: Frecuencia relativa sin b280 (n = 360)...')
    plot_figura5_frecuencia_sin_b280(df_freq_no_b280, total_no_b280)

    print('\n🎨 [4/6] Generando Figura Compuesta 2-en-1 Horizontal...')
    plot_figura_2en1_horizontal(df_freq, df_freq_no_b280, total_codes, total_no_b280)

    print('\n🎨 [5/6] Generando Figura Compuesta 3-en-1 Horizontal (Tríptico)...')
    plot_figura_3en1_horizontal(df_prev, df_freq, df_freq_no_b280, n_cases, total_codes, total_no_b280)

    print('\n🎨 [6/6] Generando Figura por Componentes CIF (b, d, e)...')
    plot_figura_componentes_cif(df_prev, df_freq, df_freq_no_b280)

    print('\n' + '=' * 80)
    print(' ✨ TODAS LAS FIGURAS HAN SIDO GENERADAS CON ÉXITO EN 300 DPI (PNG, PDF, SVG)')
    print('=' * 80)


if __name__ == '__main__':
    main()
