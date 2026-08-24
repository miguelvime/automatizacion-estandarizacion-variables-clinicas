# -*- coding: utf-8 -*-
"""
===============================================================================
GENERACIÓN DE FIGURAS Y GRÁFICOS DE DESEMPEÑO: HISTORIAS HUMANAS (TFM)
EVALUACIÓN COMPARATIVA TRI-MODELO: FLASH 3.5, FLASH 3.6 Y GEMMA-4-31B-IT
CALIDAD DE PUBLICACIÓN CIENTÍFICA (300 DPI, FORMATO APA / EDITORIAL)
===============================================================================
"""

import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
CARPETA_FIGURAS = BASE_DIR / 'results' / 'TFL' / 'figuras'
RUTA_JSON_HUMANO = BASE_DIR / 'results' / 'human_text' / 'resumen_human_annotated.json'
RUTA_JSON_SINTETICO = BASE_DIR / 'results' / 'llm_text' / 'resumen_f1_score.json'

os.makedirs(CARPETA_FIGURAS, exist_ok=True)

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9.5
plt.rcParams['ytick.labelsize'] = 9.5
plt.rcParams['legend.fontsize'] = 9.5
plt.rcParams['figure.dpi'] = 300

COLORES_MODELOS = {
    'flash_35': '#2E86C1',   # Azul profesional
    'flash_36': '#27AE60',   # Verde esmeralda
    'gemma_31b': '#E67E22'   # Ámbar / Naranja cálido
}

NOMBRES_MODELOS = {
    'flash_35': 'Gemini Flash 3.5',
    'flash_36': 'Gemini Flash 3.6',
    'gemma_31b': 'Gemma-4-31B-it (Local)'
}

def cargar_datos():
    with open(RUTA_JSON_HUMANO, 'r', encoding='utf-8') as f:
        datos_humano = json.load(f)
    with open(RUTA_JSON_SINTETICO, 'r', encoding='utf-8') as f:
        datos_sintetico = json.load(f)
    return datos_humano, datos_sintetico

def figura_01_comparativa_global(datos_humano):
    metricas = ['Micro-F1', 'Macro-F1', 'Weighted-F1', 'Exact Match (EMR)']
    x = np.arange(len(metricas))
    ancho = 0.26
    
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    
    modelos = [
        ('flash_35', NOMBRES_MODELOS['flash_35'], COLORES_MODELOS['flash_35']),
        ('flash_36', NOMBRES_MODELOS['flash_36'], COLORES_MODELOS['flash_36']),
        ('gemma_31b', NOMBRES_MODELOS['gemma_31b'], COLORES_MODELOS['gemma_31b'])
    ]
    
    for idx, (m_id, m_nom, color) in enumerate(modelos):
        d = datos_humano[m_id]
        des = d['desempeno']
        ci = d['ci_95']
        
        valores = [
            des['micro']['f1'],
            des['macro']['f1'],
            des['weighted']['f1'],
            des['emr'] / 100.0
        ]
        
        yerr_lower = [
            des['micro']['f1'] - ci['micro'][0],
            des['macro']['f1'] - ci['macro'][0],
            des['weighted']['f1'] - ci['weighted'][0],
            0
        ]
        yerr_upper = [
            ci['micro'][1] - des['micro']['f1'],
            ci['macro'][1] - des['macro']['f1'],
            ci['weighted'][1] - des['weighted']['f1'],
            0
        ]
        yerr = [yerr_lower, yerr_upper]
        
        offset = (idx - 1) * ancho
        bars = ax.bar(x + offset, valores, ancho, yerr=yerr, capsize=4,
                      label=m_nom, color=color, alpha=0.90, edgecolor='#222222', linewidth=0.8)
        
        for bar, val in zip(bars, valores):
            ax.annotate(f'{val:.3f}' if val < 1.0 else f'{val*100:.1f}%',
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.025),
                        ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    ax.set_ylabel('Puntuación / Proporción', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metricas, fontweight='bold')
    ax.set_ylim(0, 1.12)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.legend(frameon=True, facecolor='white', framealpha=0.95, loc='upper right')
    
    plt.tight_layout()
    out_p = CARPETA_FIGURAS / '01_comparativa_global_f1_human.png'
    plt.savefig(out_p, dpi=300)
    plt.close()
    print(f' [FIGURA 1 OK] {out_p}')

def figura_02_precision_recall_f1(datos_humano):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8))
    
    metricas = ['Precisión', 'Sensibilidad (Recall)', 'F1-Score']
    x = np.arange(len(metricas))
    ancho = 0.25
    
    modelos = [
        ('flash_35', NOMBRES_MODELOS['flash_35'], COLORES_MODELOS['flash_35']),
        ('flash_36', NOMBRES_MODELOS['flash_36'], COLORES_MODELOS['flash_36']),
        ('gemma_31b', NOMBRES_MODELOS['gemma_31b'], COLORES_MODELOS['gemma_31b'])
    ]
    
    for ax, nivel, titulo in [(ax1, 'micro', 'Nivel Micro (Global)'), (ax2, 'weighted', 'Nivel Weighted (Ponderado)')]:
        for idx, (m_id, m_nom, color) in enumerate(modelos):
            d = datos_humano[m_id]['desempeno'][nivel]
            valores = [d['p'], d['r'], d['f1']]
            offset = (idx - 1) * ancho
            bars = ax.bar(x + offset, valores, ancho, label=m_nom, color=color, alpha=0.90, edgecolor='#222222', linewidth=0.8)
            for bar, val in zip(bars, valores):
                ax.annotate(f'{val:.3f}', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015),
                            ha='center', va='bottom', fontsize=8, fontweight='bold')
                
        ax.set_title(titulo, fontweight='bold', pad=10)
        ax.set_ylabel('Puntuación (0 - 1)', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(metricas, fontweight='bold')
        ax.set_ylim(0, 1.10)
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        if ax == ax1:
            ax.legend(frameon=True, facecolor='white', framealpha=0.95, loc='upper right', fontsize=8.5)
            
    plt.tight_layout()
    out_p = CARPETA_FIGURAS / '02_precision_recall_f1_pareado_human.png'
    plt.savefig(out_p, dpi=300)
    plt.close()
    print(f' [FIGURA 2 OK] {out_p}')

def figura_03_auditoria_per_class(datos_humano):
    # Clases activas con soporte > 0
    p35 = datos_humano['flash_35']['desempeno']['per_class']
    p36 = datos_humano['flash_36']['desempeno']['per_class']
    pg = datos_humano['gemma_31b']['desempeno']['per_class']
    
    clases_activas = [c for c in sorted(p35.keys()) if p35[c]['soporte'] > 0]
    
    # Ordenar por soporte y código
    clases_activas.sort(key=lambda c: (p35[c]['componente'], -p35[c]['soporte']))
    
    etiquetas = [f"{c} - {p35[c]['nombre'][:34]} (N={p35[c]['soporte']})" for c in clases_activas]
    
    f1_35 = [p35[c]['f1'] for c in clases_activas]
    f1_36 = [p36[c]['f1'] for c in clases_activas]
    f1_gemma = [pg[c]['f1'] for c in clases_activas]
    
    y = np.arange(len(clases_activas))
    altura = 0.26
    
    fig, ax = plt.subplots(figsize=(10.5, 11.5))
    
    rects1 = ax.barh(y - altura, f1_35, altura, label=NOMBRES_MODELOS['flash_35'], color=COLORES_MODELOS['flash_35'], alpha=0.88, edgecolor='#222222', linewidth=0.6)
    rects2 = ax.barh(y, f1_36, altura, label=NOMBRES_MODELOS['flash_36'], color=COLORES_MODELOS['flash_36'], alpha=0.88, edgecolor='#222222', linewidth=0.6)
    rects3 = ax.barh(y + altura, f1_gemma, altura, label=NOMBRES_MODELOS['gemma_31b'], color=COLORES_MODELOS['gemma_31b'], alpha=0.88, edgecolor='#222222', linewidth=0.6)
    
    ax.set_xlabel('F1-Score', fontweight='bold')
    ax.set_yticks(y)
    ax.set_yticklabels(etiquetas, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.08)
    ax.axvline(0.80, color='#C0392B', linestyle='--', alpha=0.75, linewidth=1.2, label='Umbral Excelencia (0.80)')
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    ax.legend(frameon=True, facecolor='white', framealpha=0.95, loc='lower right', fontsize=9)
    
    plt.tight_layout()
    out_p = CARPETA_FIGURAS / '03_auditoria_per_class_human.png'
    plt.savefig(out_p, dpi=300)
    plt.close()
    print(f' [FIGURA 3 OK] {out_p}')

def figura_04_desempeno_por_componente(datos_humano):
    componentes = ['b', 'd', 'e']
    nombres_comp = ['Funciones Corporales (b)', 'Actividades y Part. (d)', 'Factores Ambientales (e)']
    
    x = np.arange(len(componentes))
    ancho = 0.25
    
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    
    modelos = [
        ('flash_35', NOMBRES_MODELOS['flash_35'], COLORES_MODELOS['flash_35']),
        ('flash_36', NOMBRES_MODELOS['flash_36'], COLORES_MODELOS['flash_36']),
        ('gemma_31b', NOMBRES_MODELOS['gemma_31b'], COLORES_MODELOS['gemma_31b'])
    ]
    
    for idx, (m_id, m_nom, color) in enumerate(modelos):
        comp_d = datos_humano[m_id]['desempeno']['por_componente']
        valores = [comp_d[c]['micro_f1'] for c in componentes]
        offset = (idx - 1) * ancho
        bars = ax.bar(x + offset, valores, ancho, label=m_nom, color=color, alpha=0.90, edgecolor='#222222', linewidth=0.8)
        for bar, val in zip(bars, valores):
            ax.annotate(f'{val:.3f}', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02),
                        ha='center', va='bottom', fontsize=8.5, fontweight='bold')
            
    ax.set_ylabel('Micro-F1 por Componente', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(nombres_comp, fontweight='bold')
    ax.set_ylim(0, 1.10)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.legend(frameon=True, facecolor='white', framealpha=0.95, loc='upper right')
    
    plt.tight_layout()
    out_p = CARPETA_FIGURAS / '04_desempeno_por_componente_cif_human.png'
    plt.savefig(out_p, dpi=300)
    plt.close()
    print(f' [FIGURA 4 OK] {out_p}')

def figura_05_comparativa_sintetico_humano(datos_humano, datos_sintetico):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 5.0))
    
    modelos_syn_map = {
        'flash_35': 'gemini_flash_35',
        'flash_36': 'gemini_flash_36',
        'gemma_31b': 'gemma_31b'
    }
    
    # Panel 1: Micro-F1 Sintético vs Humano
    modelos_lista = ['flash_35', 'flash_36', 'gemma_31b']
    labels = ['Gemini Flash 3.5', 'Gemini Flash 3.6', 'Gemma-4-31B-it']
    
    f1_syn = []
    f1_hum = []
    retenciones_f1 = []
    
    for m in modelos_lista:
        s_id = modelos_syn_map[m]
        syn_item = next(item for item in datos_sintetico if item['modelo_id'] == s_id)
        val_syn = syn_item['metricas']['micro']['f1']
        val_hum = datos_humano[m]['desempeno']['micro']['f1']
        f1_syn.append(val_syn)
        f1_hum.append(val_hum)
        retenciones_f1.append((val_hum / val_syn) * 100.0)
        
    x = np.arange(len(labels))
    ancho = 0.35
    
    rects1 = ax1.bar(x - ancho/2, f1_syn, ancho, label='Corpus Sintético (N = 114)', color='#7F8C8D', alpha=0.85, edgecolor='#222222')
    rects2 = ax1.bar(x + ancho/2, f1_hum, ancho, label='Historias Fisioterapeutas (N = 21)', color='#2980B9', alpha=0.90, edgecolor='#222222')
    
    for bar in rects1:
        ax1.annotate(f'{bar.get_height():.3f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015),
                     ha='center', va='bottom', fontsize=8, fontweight='bold')
    for bar in rects2:
        ax1.annotate(f'{bar.get_height():.3f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015),
                     ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1B4F72')
        
    ax1.set_title('A. Desempeño Diagnóstico (Micro-F1)', fontweight='bold', pad=10)
    ax1.set_ylabel('Micro-F1 (0 - 1)', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontweight='bold', fontsize=8.5)
    ax1.set_ylim(0, 1.12)
    ax1.grid(axis='y', linestyle='--', alpha=0.4)
    ax1.legend(frameon=True, facecolor='white', framealpha=0.95, loc='lower right', fontsize=8.5)
    
    # Panel 2: Tasa de Retención Métricas Clave
    metricas_ret = ['Micro-F1', 'Precisión', 'Recall', 'EMR', 'AC1 Gwet']
    x2 = np.arange(len(metricas_ret))
    ancho2 = 0.25
    
    for idx, (m_id, m_nom, color) in enumerate([
        ('flash_35', NOMBRES_MODELOS['flash_35'], COLORES_MODELOS['flash_35']),
        ('flash_36', NOMBRES_MODELOS['flash_36'], COLORES_MODELOS['flash_36']),
        ('gemma_31b', NOMBRES_MODELOS['gemma_31b'], COLORES_MODELOS['gemma_31b'])
    ]):
        s_id = modelos_syn_map[m_id]
        syn_item = next(item for item in datos_sintetico if item['modelo_id'] == s_id)
        d_hum = datos_humano[m_id]
        
        # synthetic values
        s_mf1 = syn_item['metricas']['micro']['f1']
        s_prec = syn_item['metricas']['micro']['precision']
        s_rec = syn_item['metricas']['micro']['recall']
        s_emr = syn_item['metricas']['emr_pct']
        s_ac1 = 0.9994 if m_id != 'flash_36' else 1.0000
        
        # human values
        h_mf1 = d_hum['desempeno']['micro']['f1']
        h_prec = d_hum['desempeno']['micro']['p']
        h_rec = d_hum['desempeno']['micro']['r']
        h_emr = d_hum['desempeno']['emr']
        h_ac1 = d_hum['fiabilidad']['ac1']
        
        ret_vals = [
            (h_mf1 / s_mf1) * 100.0,
            (h_prec / s_prec) * 100.0,
            (h_rec / s_rec) * 100.0,
            (h_emr / s_emr) * 100.0,
            (h_ac1 / s_ac1) * 100.0
        ]
        
        offset2 = (idx - 1) * ancho2
        bars = ax2.bar(x2 + offset2, ret_vals, ancho2, label=m_nom, color=color, alpha=0.90, edgecolor='#222222', linewidth=0.8)
        for bar, val in zip(bars, ret_vals):
            ax2.annotate(f'{val:.1f}%', xy=(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5),
                         ha='center', va='bottom', fontsize=7.5, fontweight='bold')
            
    ax2.set_title('B. Tasa de Retención del Rendimiento (%)', fontweight='bold', pad=10)
    ax2.set_ylabel('Tasa de Retención (%)', fontweight='bold')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(metricas_ret, fontweight='bold', fontsize=8.5)
    ax2.set_ylim(0, 115)
    ax2.axhline(100.0, color='#7F8C8D', linestyle=':', alpha=0.7)
    ax2.grid(axis='y', linestyle='--', alpha=0.4)
    ax2.legend(frameon=True, facecolor='white', framealpha=0.95, loc='upper right', fontsize=8)
    
    plt.tight_layout()
    out_p = CARPETA_FIGURAS / '05_comparativa_sintetico_vs_humano.png'
    plt.savefig(out_p, dpi=300)
    plt.close()
    print(f' [FIGURA 5 OK] {out_p}')

if __name__ == '__main__':
    dh, ds = cargar_datos()
    figura_01_comparativa_global(dh)
    figura_02_precision_recall_f1(dh)
    figura_03_auditoria_per_class(dh)
    figura_04_desempeno_por_componente(dh)
    figura_05_comparativa_sintetico_humano(dh, ds)
    print('[OK] Todas las figuras tri-modelo generadas exitosamente.')
