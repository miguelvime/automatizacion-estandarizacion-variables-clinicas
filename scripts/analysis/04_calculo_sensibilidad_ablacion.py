# -*- coding: utf-8 -*-
"""
===============================================================================
CÁLCULO DE SENSIBILIDAD Y ABLACIÓN DE LA CLASE DOMINANTE (stats_v4)
EVALUACIÓN COMPARATIVA MULTIMODELO (GEMMA 31B, FLASH 3.5, FLASH 3.7)
===============================================================================

¿Qué calcula este script?
-------------------------
Evalúa la robustez del rendimiento diagnóstico excluyendo la categoría clínica
dominante (b280 - Sensación de dolor, presente en el 92.1% de historias clínicas)
en los 3 modelos LLM evaluados.

Calcula para cada modelo:
1. Dataset Completo (24 códigos, 465 menciones reales)
2. Ablación sin b280 (23 códigos, 360 menciones reales)
3. Variación Absoluta (Δ = Sin - Con)
4. Tasa de Retención del Rendimiento ([Sin b280 / Con b280] * 100)

Salidas:
- resumen_ablacion.json
- tabla_sensibilidad_ablacion.csv
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
LLM_DIR = BASE_DIR / "results" / "llm_text"
TFL_DIR = BASE_DIR / "results" / "TFL"
TABLAS_DIR = TFL_DIR / "tablas"

MODELOS = [
    {
        "id": "gemma_31b",
        "nombre": "Gemma-4-31B-it",
        "archivo": LLM_DIR / "2026-08-25_gemma_codified.json"
    },
    {
        "id": "gemini_flash_35",
        "nombre": "Gemini Flash 3.5",
        "archivo": LLM_DIR / "2026-08-25-flash-3.5-codified.json"
    },
    {
        "id": "gemini_flash_37",
        "nombre": "Gemini Flash 3.7",
        "archivo": LLM_DIR / "2026-08-25-3.7-flash-codified.json"
    }
]


def calcular_metricas_espacio(datos: List[Dict[str, Any]], codigos_a_excluir: Set[str] = None) -> Dict[str, Any]:
    """Calcula las métricas de rendimiento multietiqueta permitiendo excluir códigos (p.ej. b280)."""
    if codigos_a_excluir is None:
        codigos_a_excluir = set()

    n_docs = len(datos)
    total_tp = 0
    total_fp = 0
    total_fn = 0
    emr_aciertos = 0

    todos_codigos = set()
    for item in datos:
        gt_filtrado = [c for c in item.get("icf_codes", []) if c not in codigos_a_excluir]
        pred_filtrado = [c for c in item.get("predicted_icf_codes_consensus", []) if c not in codigos_a_excluir]
        todos_codigos.update(gt_filtrado)
        todos_codigos.update(pred_filtrado)

    lista_codigos = sorted(list(todos_codigos))
    total_menciones_gt = 0

    for item in datos:
        gt_set = set([c for c in item.get("icf_codes", []) if c not in codigos_a_excluir])
        pred_set = set([c for c in item.get("predicted_icf_codes_consensus", []) if c not in codigos_a_excluir])

        total_menciones_gt += len(gt_set)

        if gt_set == pred_set:
            emr_aciertos += 1

        tp_doc = len(gt_set & pred_set)
        fp_doc = len(pred_set - gt_set)
        fn_doc = len(gt_set - pred_set)

        total_tp += tp_doc
        total_fp += fp_doc
        total_fn += fn_doc

    p_micro = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    r_micro = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    f1_micro = (2.0 * p_micro * r_micro) / (p_micro + r_micro) if (p_micro + r_micro) > 0 else 0.0

    f1_clases = []
    soportes = []
    for c in lista_codigos:
        tp_c = sum(1 for item in datos if c in item.get("icf_codes", []) and c not in codigos_a_excluir and c in item.get("predicted_icf_codes_consensus", []))
        fp_c = sum(1 for item in datos if c not in item.get("icf_codes", []) and c not in codigos_a_excluir and c in item.get("predicted_icf_codes_consensus", []))
        fn_c = sum(1 for item in datos if c in item.get("icf_codes", []) and c not in codigos_a_excluir and c not in item.get("predicted_icf_codes_consensus", []))

        soporte = tp_c + fn_c
        denom = (2 * tp_c) + fp_c + fn_c
        f1_c = (2.0 * tp_c) / denom if denom > 0 else (1.0 if (soporte == 0 and fp_c == 0) else 0.0)

        f1_clases.append(f1_c)
        soportes.append(soporte)

    macro_f1 = float(np.mean(f1_clases)) if len(f1_clases) > 0 else 0.0
    tot_s = sum(soportes)
    weighted_f1 = float(sum(f * s for f, s in zip(f1_clases, soportes)) / tot_s) if tot_s > 0 else 0.0
    emr = float(emr_aciertos / n_docs) if n_docs > 0 else 0.0

    return {
        "N_Codigos": len(lista_codigos),
        "Menciones_GT": total_menciones_gt,
        "Micro_F1": float(f1_micro),
        "Micro_Precision": float(p_micro),
        "Micro_Recall": float(r_micro),
        "Macro_F1": float(macro_f1),
        "Weighted_F1": float(weighted_f1),
        "EMR": float(emr),
        "EMR_Aciertos": emr_aciertos,
        "TP": total_tp,
        "FP": total_fp,
        "FN": total_fn
    }


def ejecutar_analisis_ablacion():
    print("=" * 80)
    print("🔬 [stats_v4] ANÁLISIS DE SENSIBILIDAD Y ABLACIÓN DE LA CLASE DOMINANTE (b280)")
    print("=" * 80)

    resultados = {}

    for mod in MODELOS:
        with open(mod["archivo"], "r", encoding="utf-8") as f:
            datos = json.load(f)

        completo = calcular_metricas_espacio(datos, codigos_a_excluir=set())
        ablado = calcular_metricas_espacio(datos, codigos_a_excluir={"b280"})

        delta = {
            "Micro_F1": ablado["Micro_F1"] - completo["Micro_F1"],
            "Micro_Precision": ablado["Micro_Precision"] - completo["Micro_Precision"],
            "Micro_Recall": ablado["Micro_Recall"] - completo["Micro_Recall"],
            "Macro_F1": ablado["Macro_F1"] - completo["Macro_F1"],
            "Weighted_F1": ablado["Weighted_F1"] - completo["Weighted_F1"],
            "EMR": ablado["EMR"] - completo["EMR"]
        }

        retencion = {
            "Micro_F1": (ablado["Micro_F1"] / completo["Micro_F1"]) * 100 if completo["Micro_F1"] > 0 else 0.0,
            "Micro_Precision": (ablado["Micro_Precision"] / completo["Micro_Precision"]) * 100 if completo["Micro_Precision"] > 0 else 0.0,
            "Micro_Recall": (ablado["Micro_Recall"] / completo["Micro_Recall"]) * 100 if completo["Micro_Recall"] > 0 else 0.0,
            "Macro_F1": (ablado["Macro_F1"] / completo["Macro_F1"]) * 100 if completo["Macro_F1"] > 0 else 0.0,
            "Weighted_F1": (ablado["Weighted_F1"] / completo["Weighted_F1"]) * 100 if completo["Weighted_F1"] > 0 else 0.0,
            "EMR": (ablado["EMR"] / completo["EMR"]) * 100 if completo["EMR"] > 0 else 0.0
        }

        resultados[mod["id"]] = {
            "nombre": mod["nombre"],
            "completo": completo,
            "ablado": ablado,
            "delta": delta,
            "retencion": retencion
        }

        print(f"\n▶ Modelo: {mod['nombre']}")
        print(f"   * Completo (Con b280): Micro-F1 = {completo['Micro_F1']:.4f} | Macro-F1 = {completo['Macro_F1']:.4f} | EMR = {completo['EMR']*100:.2f}% ({completo['EMR_Aciertos']}/114)")
        print(f"   * Ablación (Sin b280): Micro-F1 = {ablado['Micro_F1']:.4f} | Macro-F1 = {ablado['Macro_F1']:.4f} | EMR = {ablado['EMR']*100:.2f}% ({ablado['EMR_Aciertos']}/114)")
        print(f"   * Retención:           Micro = {retencion['Micro_F1']:.2f}% | Macro = {retencion['Macro_F1']:.2f}% | EMR = {retencion['EMR']:.2f}%")
        print(f"   * Variación (Δ):       dMicro = {delta['Micro_F1']:+.4f} | dMacro = {delta['Macro_F1']:+.4f} | dEMR = {delta['EMR']*100:+.2f}%")

    # Guardar JSON
    ruta_json = LLM_DIR / "resumen_ablacion.json"
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Resumen JSON guardado en: {ruta_json}")

    # Construir DataFrame en Formato APA / Transpuesto (Modelos en Columnas)
    filas_tabla = [
        # BLOQUE 1: CORPUS Y ESPACIO
        ("Parámetros del Espacio", "Número de Categorías CIF evaluadas", "24 códigos", "24 códigos", "24 códigos"),
        ("Parámetros del Espacio", "Soporte Real Ground Truth (menciones)", "465", "465", "465"),
        ("Parámetros del Espacio", "Prevalencia de b280 en el Corpus", "92.1% (105/114)", "92.1% (105/114)", "92.1% (105/114)"),

        # BLOQUE 2: DATASET COMPLETO (CON b280)
        ("Espacio Completo (Con b280)", "Micro-F1", f"{resultados['gemma_31b']['completo']['Micro_F1']:.4f}", f"{resultados['gemini_flash_35']['completo']['Micro_F1']:.4f}", f"{resultados['gemini_flash_37']['completo']['Micro_F1']:.4f}"),
        ("Espacio Completo (Con b280)", "Macro-F1", f"{resultados['gemma_31b']['completo']['Macro_F1']:.4f}", f"{resultados['gemini_flash_35']['completo']['Macro_F1']:.4f}", f"{resultados['gemini_flash_37']['completo']['Macro_F1']:.4f}"),
        ("Espacio Completo (Con b280)", "Weighted-F1", f"{resultados['gemma_31b']['completo']['Weighted_F1']:.4f}", f"{resultados['gemini_flash_35']['completo']['Weighted_F1']:.4f}", f"{resultados['gemini_flash_37']['completo']['Weighted_F1']:.4f}"),
        ("Espacio Completo (Con b280)", "Exact Match Ratio (EMR %)", f"{resultados['gemma_31b']['completo']['EMR']*100:.2f}% ({resultados['gemma_31b']['completo']['EMR_Aciertos']}/114)", f"{resultados['gemini_flash_35']['completo']['EMR']*100:.2f}% ({resultados['gemini_flash_35']['completo']['EMR_Aciertos']}/114)", f"{resultados['gemini_flash_37']['completo']['EMR']*100:.2f}% ({resultados['gemini_flash_37']['completo']['EMR_Aciertos']}/114)"),
        ("Espacio Completo (Con b280)", "Matriz de Confusión (TP / FP / FN)", f"{resultados['gemma_31b']['completo']['TP']} / {resultados['gemma_31b']['completo']['FP']} / {resultados['gemma_31b']['completo']['FN']}", f"{resultados['gemini_flash_35']['completo']['TP']} / {resultados['gemini_flash_35']['completo']['FP']} / {resultados['gemini_flash_35']['completo']['FN']}", f"{resultados['gemini_flash_37']['completo']['TP']} / {resultados['gemini_flash_37']['completo']['FP']} / {resultados['gemini_flash_37']['completo']['FN']}"),

        # BLOQUE 3: ABLACIÓN (SIN b280)
        ("Ablación (Sin dolor b280)", "Micro-F1", f"{resultados['gemma_31b']['ablado']['Micro_F1']:.4f}", f"{resultados['gemini_flash_35']['ablado']['Micro_F1']:.4f}", f"{resultados['gemini_flash_37']['ablado']['Micro_F1']:.4f}"),
        ("Ablación (Sin dolor b280)", "Macro-F1", f"{resultados['gemma_31b']['ablado']['Macro_F1']:.4f}", f"{resultados['gemini_flash_35']['ablado']['Macro_F1']:.4f}", f"{resultados['gemini_flash_37']['ablado']['Macro_F1']:.4f}"),
        ("Ablación (Sin dolor b280)", "Weighted-F1", f"{resultados['gemma_31b']['ablado']['Weighted_F1']:.4f}", f"{resultados['gemini_flash_35']['ablado']['Weighted_F1']:.4f}", f"{resultados['gemini_flash_37']['ablado']['Weighted_F1']:.4f}"),
        ("Ablación (Sin dolor b280)", "Exact Match Ratio (EMR %)", f"{resultados['gemma_31b']['ablado']['EMR']*100:.2f}% ({resultados['gemma_31b']['ablado']['EMR_Aciertos']}/114)", f"{resultados['gemini_flash_35']['ablado']['EMR']*100:.2f}% ({resultados['gemini_flash_35']['ablado']['EMR_Aciertos']}/114)", f"{resultados['gemini_flash_37']['ablado']['EMR']*100:.2f}% ({resultados['gemini_flash_37']['ablado']['EMR_Aciertos']}/114)"),
        ("Ablación (Sin dolor b280)", "Matriz de Confusión (TP / FP / FN)", f"{resultados['gemma_31b']['ablado']['TP']} / {resultados['gemma_31b']['ablado']['FP']} / {resultados['gemma_31b']['ablado']['FN']}", f"{resultados['gemini_flash_35']['ablado']['TP']} / {resultados['gemini_flash_35']['ablado']['FP']} / {resultados['gemini_flash_35']['ablado']['FN']}", f"{resultados['gemini_flash_37']['ablado']['TP']} / {resultados['gemini_flash_37']['ablado']['FP']} / {resultados['gemini_flash_37']['ablado']['FN']}"),

        # BLOQUE 4: DIFERENCIA ABSOLUTA (Δ = SIN - CON)
        ("Variación Absoluta (Δ = Sin - Con)", "Δ Micro-F1", f"{resultados['gemma_31b']['delta']['Micro_F1']:+.4f}", f"{resultados['gemini_flash_35']['delta']['Micro_F1']:+.4f}", f"{resultados['gemini_flash_37']['delta']['Micro_F1']:+.4f}"),
        ("Variación Absoluta (Δ = Sin - Con)", "Δ Macro-F1", f"{resultados['gemma_31b']['delta']['Macro_F1']:+.4f}", f"{resultados['gemini_flash_35']['delta']['Macro_F1']:+.4f}", f"{resultados['gemini_flash_37']['delta']['Macro_F1']:+.4f}"),
        ("Variación Absoluta (Δ = Sin - Con)", "Δ Weighted-F1", f"{resultados['gemma_31b']['delta']['Weighted_F1']:+.4f}", f"{resultados['gemini_flash_35']['delta']['Weighted_F1']:+.4f}", f"{resultados['gemini_flash_37']['delta']['Weighted_F1']:+.4f}"),
        ("Variación Absoluta (Δ = Sin - Con)", "Δ EMR (%)", f"{resultados['gemma_31b']['delta']['EMR']*100:+.2f}%", f"{resultados['gemini_flash_35']['delta']['EMR']*100:+.2f}%", f"{resultados['gemini_flash_37']['delta']['EMR']*100:+.2f}%"),

        # BLOQUE 5: TASA DE RETENCIÓN DEL RENDIMIENTO (%)
        ("Tasa de Retención (%)", "Retención Micro-F1", f"{resultados['gemma_31b']['retencion']['Micro_F1']:.2f}%", f"{resultados['gemini_flash_35']['retencion']['Micro_F1']:.2f}%", f"{resultados['gemini_flash_37']['retencion']['Micro_F1']:.2f}%"),
        ("Tasa de Retención (%)", "Retención Macro-F1", f"{resultados['gemma_31b']['retencion']['Macro_F1']:.2f}%", f"{resultados['gemini_flash_35']['retencion']['Macro_F1']:.2f}%", f"{resultados['gemini_flash_37']['retencion']['Macro_F1']:.2f}%"),
        ("Tasa de Retención (%)", "Retención Weighted-F1", f"{resultados['gemma_31b']['retencion']['Weighted_F1']:.2f}%", f"{resultados['gemini_flash_35']['retencion']['Weighted_F1']:.2f}%", f"{resultados['gemini_flash_37']['retencion']['Weighted_F1']:.2f}%"),
        ("Tasa de Retención (%)", "Retención EMR", f"{resultados['gemma_31b']['retencion']['EMR']:.2f}%", f"{resultados['gemini_flash_35']['retencion']['EMR']:.2f}%", f"{resultados['gemini_flash_37']['retencion']['EMR']:.2f}%")
    ]

    df_tabla = pd.DataFrame(filas_tabla, columns=[
        "Dimensión",
        "Métrica / Parámetro",
        "Gemma-4-31B-it",
        "Gemini Flash 3.5",
        "Gemini Flash 3.7"
    ])

    ruta_csv = TABLAS_DIR / "tabla_sensibilidad_ablacion.csv"
    df_tabla.to_csv(ruta_csv, index=False, encoding="utf-8-sig")
    print(f"[OK] Tabla CSV guardada en: {ruta_csv}")

    return resultados, df_tabla


if __name__ == "__main__":
    ejecutar_analisis_ablacion()
