# -*- coding: utf-8 -*-
"""
===============================================================================
GENERACIÓN DE FIGURAS Y GRÁFICOS DE DESEMPEÑO DIAGNÓSTICO (stats_v4)
CALIDAD DE PUBLICACIÓN CIENTÍFICA (300 DPI)
===============================================================================

Este script genera las figuras visuales comparativas de validez diagnóstica y
rendimiento F1-score entre los 3 modelos LLM evaluados:
1. Gemma-4-31B-it
2. Gemini Flash 3.5
3. Gemini Flash 3.7

Figuras generadas en `results/stats_v4/figuras/`:
-------------------------------------------------
1. `01_comparativa_global_f1_modelos.png`: Comparativa de F1 (Micro, Macro, Weighted) y Exact Match con IC 95%.
2. `02_precision_recall_f1_pareado.png`: Desglose pareado de Precisión, Recall y F1 por modelo.
3. `03_auditoria_per_class_24_codigos.png`: Barras horizontales de F1 por código CIF (24 categorías del Core Set).
4. `04_desempeno_por_capitulo_cif.png`: Rendimiento comparativo por componentes CIF (b: Cuerpo, d: Actividades, e: Ambiente).
5. `05_matriz_confusion_tp_fp_fn.png`: Desglose global de Verdaderos Positivos, Falsos Positivos y Falsos Negativos.
"""

import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
LLM_DIR = BASE_DIR / "results" / "llm_text"
TFL_DIR = BASE_DIR / "results" / "TFL"
CARPETA_FIGURAS = TFL_DIR / "figuras"
RUTA_JSON = LLM_DIR / "resumen_f1_score.json"

os.makedirs(CARPETA_FIGURAS, exist_ok=True)

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 14
plt.rcParams['figure.dpi'] = 300

COLORES_MODELOS = {
    "gemma_31b": "#1F4E79",       # Azul oscuro elegante
    "gemini_flash_35": "#4B77BE",  # Azul medio
    "gemini_flash_37": "#27AE60"   # Verde esmeralda
}


def cargar_datos():
    if not RUTA_JSON.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {RUTA_JSON}")
    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        datos = json.load(f)
    return datos


def figura_01_comparativa_global(datos):
    metricas = ["Micro-F1", "Macro-F1", "Weighted-F1", "Exact Match (EMR)"]
    x = np.arange(len(metricas))
    ancho = 0.26
    
    fig, ax = plt.subplots(figsize=(10, 5.5))
    
    for idx, d in enumerate(datos):
        m_id = d["modelo_id"]
        m_nom = d["modelo_nombre"]
        color = COLORES_MODELOS.get(m_id, "#333333")
        
        m = d["metricas"]
        ci = d["ci_95"]
        
        vals = [
            m["micro"]["f1"],
            m["macro"]["f1"],
            m["weighted"]["f1"],
            m["emr_pct"] / 100.0
        ]
        
        yerr_low = [
            vals[0] - ci["micro_f1"][0],
            vals[1] - ci["macro_f1"][0],
            vals[2] - ci["weighted_f1"][0],
            0
        ]
        yerr_high = [
            ci["micro_f1"][1] - vals[0],
            ci["macro_f1"][1] - vals[1],
            ci["weighted_f1"][1] - vals[2],
            0
        ]
        
        offset = (idx - 1) * ancho
        barras = ax.bar(x + offset, vals, width=ancho, yerr=[yerr_low, yerr_high],
                        capsize=4, label=m_nom, color=color, alpha=0.88, edgecolor="black", linewidth=0.7)
        
        for bar, val in zip(barras, vals):
            y_pos = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., y_pos + 0.02,
                    f"{val:.2f}" if val < 1.0 else f"{val:.1f}",
                    ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    ax.set_ylabel("Puntuación / Proporción (0 a 1)", fontweight='bold')
#     ax.set_title("Comparativa Global de Desempeño Diagnóstico (F1-Score e Intervalos 95% Bootstrap)", fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(metricas, fontweight='bold')
    ax.set_ylim(0.70, 1.05)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    ax.legend(frameon=True, facecolor='#F8F9F9', edgecolor='#BDC3C7', loc="lower right")
    
    plt.tight_layout()
    ruta_salida = CARPETA_FIGURAS / "01_comparativa_global_f1_modelos.png"
    plt.savefig(ruta_salida, dpi=300)
    plt.close()
    print(f" [OK] Figura 1 guardada: {ruta_salida}")


def figura_02_precision_recall_f1(datos):
    niveles = ["Precisión Micro", "Recall Micro", "Micro-F1"]
    x = np.arange(len(niveles))
    ancho = 0.26
    
    fig, ax = plt.subplots(figsize=(9, 5))
    
    for idx, d in enumerate(datos):
        m_id = d["modelo_id"]
        m_nom = d["modelo_nombre"]
        color = COLORES_MODELOS.get(m_id, "#333333")
        m = d["metricas"]["micro"]
        
        vals = [m["precision"], m["recall"], m["f1"]]
        offset = (idx - 1) * ancho
        barras = ax.bar(x + offset, vals, width=ancho, label=m_nom, color=color, alpha=0.88, edgecolor="black", linewidth=0.7)
        
        for bar, val in zip(barras, vals):
            y_pos = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., y_pos + 0.005,
                    f"{val*100:.2f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    ax.set_ylabel("Rendimiento (%)", fontweight='bold')
#     ax.set_title("Eficacia Diagnóstica Global (Precisión, Sensibilidad y F1 a Nivel Micro)", fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(niveles, fontweight='bold')
    ax.set_ylim(0.90, 1.02)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    ax.legend(frameon=True, facecolor='#F8F9F9', edgecolor='#BDC3C7', loc="lower left")
    
    plt.tight_layout()
    ruta_salida = CARPETA_FIGURAS / "02_precision_recall_f1_pareado.png"
    plt.savefig(ruta_salida, dpi=300)
    plt.close()
    print(f" [OK] Figura 2 guardada: {ruta_salida}")


def figura_03_auditoria_per_class(datos):
    gemma = next(r for r in datos if r["modelo_id"] == "gemma_31b")
    g35 = next(r for r in datos if r["modelo_id"] == "gemini_flash_35")
    g36 = next(r for r in datos if r["modelo_id"] == "gemini_flash_37")
    
    gemma_clases = gemma["metricas"]["por_clase"]
    g35_clases = g35["metricas"]["por_clase"]
    g36_clases = g36["metricas"]["por_clase"]
    
    codigos = sorted(list(gemma_clases.keys()), reverse=True)
    y = np.arange(len(codigos))
    ancho = 0.28
    
    etiquetas = []
    f1_gemma = []
    f1_g35 = []
    f1_g36 = []
    
    for c in codigos:
        nom = gemma_clases[c]["nombre"]
        sup = gemma_clases[c]["soporte"]
        nom_corto = nom[:32] + "..." if len(nom) > 32 else nom
        etiquetas.append(f"{c} (n={sup}) - {nom_corto}")
        
        f1_gemma.append(gemma_clases[c]["f1"])
        f1_g35.append(g35_clases[c]["f1"])
        f1_g36.append(g36_clases[c]["f1"])
        
    fig, ax = plt.subplots(figsize=(12, 11))
    
    ax.barh(y + ancho, f1_gemma, height=ancho, label="Gemma-4-31B-it", color=COLORES_MODELOS["gemma_31b"], alpha=0.88, edgecolor="black", linewidth=0.5)
    ax.barh(y, f1_g35, height=ancho, label="Gemini Flash 3.5", color=COLORES_MODELOS["gemini_flash_35"], alpha=0.88, edgecolor="black", linewidth=0.5)
    ax.barh(y - ancho, f1_g36, height=ancho, label="Gemini Flash 3.7", color=COLORES_MODELOS["gemini_flash_37"], alpha=0.88, edgecolor="black", linewidth=0.5)
    
    ax.set_xlabel("F1-Score por Categoría CIF", fontweight='bold')
#     ax.set_title("Auditoría Individualizada Per Class (24 Categorías CIF del Core Set de Dolor Crónico)", fontweight='bold', pad=15)
    ax.set_yticks(y)
    ax.set_yticklabels(etiquetas, fontsize=8.5)
    ax.set_xlim(0, 1.08)
    ax.grid(axis='x', linestyle=':', alpha=0.6)
    ax.legend(frameon=True, facecolor='#F8F9F9', edgecolor='#BDC3C7', loc="lower right")
    
    plt.tight_layout()
    ruta_salida = CARPETA_FIGURAS / "03_auditoria_per_class_24_codigos.png"
    plt.savefig(ruta_salida, dpi=300)
    plt.close()
    print(f" [OK] Figura 3 guardada: {ruta_salida}")


def figura_04_desempeno_por_capitulo(datos):
    capitulos = [
        ("b", "Funciones Corporales (b)\n[11 códigos]"),
        ("d", "Actividades y Participación (d)\n[11 códigos]"),
        ("e", "Factores Ambientales (e)\n[5 códigos]")
    ]
    x = np.arange(len(capitulos))
    ancho = 0.26
    
    fig, ax = plt.subplots(figsize=(9.5, 5))
    
    for idx, d in enumerate(datos):
        m_id = d["modelo_id"]
        m_nom = d["modelo_nombre"]
        color = COLORES_MODELOS.get(m_id, "#333333")
        clases = d["metricas"]["por_clase"]
        
        f1_capitulos = []
        for pref, _ in capitulos:
            cods_cap = [c for c in clases.keys() if c.startswith(pref)]
            sup_cap = sum(clases[c]["soporte"] for c in cods_cap)
            if sup_cap > 0:
                f1_w = sum(clases[c]["f1"] * clases[c]["soporte"] for c in cods_cap) / sup_cap
            else:
                f1_w = 0.0
            f1_capitulos.append(f1_w)
            
        offset = (idx - 1) * ancho
        barras = ax.bar(x + offset, f1_capitulos, width=ancho, label=m_nom, color=color, alpha=0.88, edgecolor="black", linewidth=0.7)
        
        for bar, val in zip(barras, f1_capitulos):
            y_pos = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., y_pos + 0.01,
                    f"{val:.2f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    ax.set_ylabel("F1-Score Ponderado por Componente", fontweight='bold')
#     ax.set_title("Desempeño Diagnóstico por Componentes de la Clasificación CIF (OMS)", fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([c[1] for c in capitulos], fontweight='bold')
    ax.set_ylim(0.85, 1.05)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    ax.legend(frameon=True, facecolor='#F8F9F9', edgecolor='#BDC3C7', loc="lower right")
    
    plt.tight_layout()
    ruta_salida = CARPETA_FIGURAS / "04_desempeno_por_capitulo_cif.png"
    plt.savefig(ruta_salida, dpi=300)
    plt.close()
    print(f" [OK] Figura 4 guardada: {ruta_salida}")


def figura_05_matriz_confusion(datos):
    modelos_nom = [d["modelo_nombre"] for d in datos]
    x = np.arange(len(modelos_nom))
    ancho = 0.55
    
    tps = [d["metricas"]["confusion_global"]["tp"] for d in datos]
    fps = [d["metricas"]["confusion_global"]["fp"] for d in datos]
    fns = [d["metricas"]["confusion_global"]["fn"] for d in datos]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), gridspec_kw={'width_ratios': [1.3, 1]})
    
    barras_tp = ax1.bar(x, tps, width=ancho, color=["#1F4E79", "#4B77BE", "#27AE60"], alpha=0.88, edgecolor="black", linewidth=0.8)
    ax1.set_ylabel("Instancias Correctas (TP)", fontweight='bold')
    ax1.set_title("Aciertos Diagnósticos (Verdaderos Positivos / 465)", fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(modelos_nom, fontsize=9.0, fontweight='bold')
    ax1.set_ylim(400, 475)
    ax1.grid(axis='y', linestyle=':', alpha=0.6)
    
    for bar in barras_tp:
        y_pos = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., y_pos + 1.5,
                 f"{int(y_pos)} / 465\n({y_pos/465*100:.1f}%)", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
        
    ancho_err = 0.35
    b_fp = ax2.bar(x - ancho_err/2, fps, width=ancho_err, label="Falsos Positivos (Alucinaciones)", color="#E74C3C", alpha=0.85, edgecolor="black", linewidth=0.7)
    b_fn = ax2.bar(x + ancho_err/2, fns, width=ancho_err, label="Falsos Negativos (Omisiones)", color="#E67E22", alpha=0.85, edgecolor="black", linewidth=0.7)
    
    ax2.set_ylabel("Número de Errores", fontweight='bold')
    ax2.set_title("Auditoría de Errores (FP vs FN)", fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(modelos_nom, fontsize=9.0, fontweight='bold')
    ax2.set_ylim(0, 20)
    ax2.grid(axis='y', linestyle=':', alpha=0.6)
    ax2.legend(frameon=True, facecolor='#F8F9F9', edgecolor='#BDC3C7', loc="upper right")
    
    for bar in b_fp:
        y_pos = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., y_pos + 0.4,
                 f"{int(y_pos)}", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
    for bar in b_fn:
        y_pos = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., y_pos + 0.4,
                 f"{int(y_pos)}", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
        
    plt.tight_layout()
    ruta_salida = CARPETA_FIGURAS / "05_matriz_confusion_tp_fp_fn.png"
    plt.savefig(ruta_salida, dpi=300)
    plt.close()
    print(f" [OK] Figura 5 guardada: {ruta_salida}")


def main():
    print("=" * 75)
    print(" 🎨 GENERACIÓN DE FIGURAS ESTADÍSTICAS Y GRÁFICOS COMPARATIVOS (stats_v4)")
    print("=" * 75)
    
    datos = cargar_datos()
    
    figura_01_comparativa_global(datos)
    figura_02_precision_recall_f1(datos)
    figura_03_auditoria_per_class(datos)
    figura_04_desempeno_por_capitulo(datos)
    figura_05_matriz_confusion(datos)
    
    print("\n✅ Todas las figuras se han generado exitosamente en:")
    print(f"   📁 {CARPETA_FIGURAS}")


if __name__ == "__main__":
    main()
