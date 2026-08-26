# -*- coding: utf-8 -*-
"""
===============================================================================
CÁLCULO DE CONFIABILIDAD Y REPRODUCIBILIDAD INTER-ITERACIONES (K = 3)
MATRIZ ONTOLÓGICA COMPLETA DEL CORE SET CIF (114 HISTORIAS x 24 CÓDIGOS)
===============================================================================

¿Qué calcula este script?
-------------------------
Calcula la reproducibilidad intra-modelo estricta a través de las 3 iteraciones (K=3)
sin intervención del Ground Truth (los médicos), evaluando el espacio completo de 
decisión del Core Set CIF de dolor crónico generalizado:
- Total unidades evaluadas = 114 historias x 24 códigos CIF = 2.736 decisiones binarias.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LLM_DIR = BASE_DIR / "results" / "llm_text"

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


def obtener_codigos_core_set(archivos):
    """Extrae la lista unificada de los 24 códigos CIF del Core Set."""
    codigos = set()
    for m in archivos:
        if m["archivo"].exists():
            with open(m["archivo"], "r", encoding="utf-8") as f:
                datos = json.load(f)
                for item in datos:
                    codigos.update(item.get("icf_codes", []))
                    codigos.update(item.get("predicted_icf_it1", []))
                    codigos.update(item.get("predicted_icf_it2", []))
                    codigos.update(item.get("predicted_icf_it3", []))
    return sorted(list(codigos))


def analizar_confiabilidad_modelo(ruta_archivo: Path, nombre_modelo: str, codigos_cif: list, modelo_id: str):
    """Calcula las métricas de fiabilidad sobre la matriz ontológica completa."""
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        historias = json.load(f)

    total_historias = len(historias)
    acuerdos_exactos_historia = 0

    # 1. Acuerdo exacto a nivel de historia clínica
    for historia in historias:
        it1 = set(historia.get("predicted_icf_it1", []))
        it2 = set(historia.get("predicted_icf_it2", []))
        it3 = set(historia.get("predicted_icf_it3", []))
        if it1 == it2 == it3:
            acuerdos_exactos_historia += 1

    emr_paciente = (acuerdos_exactos_historia / total_historias) * 100.0

    # 2. Matriz Ontológica Completa (114 historias x 24 códigos = 2.736 decisiones)
    matriz_votos = []
    filas_111 = 0
    filas_000 = 0
    filas_desacuerdo = 0

    for historia in historias:
        it1 = set(historia.get("predicted_icf_it1", []))
        it2 = set(historia.get("predicted_icf_it2", []))
        it3 = set(historia.get("predicted_icf_it3", []))

        for codigo in codigos_cif:
            v1 = 1 if codigo in it1 else 0
            v2 = 1 if codigo in it2 else 0
            v3 = 1 if codigo in it3 else 0
            matriz_votos.append([v1, v2, v3])

            suma = v1 + v2 + v3
            if suma == 3:
                filas_111 += 1
            elif suma == 0:
                filas_000 += 1
            else:
                filas_desacuerdo += 1

    N = len(matriz_votos)
    K = 3                  # 3 iteraciones

    # 3. Cálculo de Po (Acuerdo Observado)
    sumatoria_acuerdo = 0.0
    total_unos = 0
    total_ceros = 0

    for fila in matriz_votos:
        n1 = sum(fila)
        n0 = K - n1
        total_unos += n1
        total_ceros += n0
        acuerdo_fila = (n1 * (n1 - 1) + n0 * (n0 - 1)) / (K * (K - 1))
        sumatoria_acuerdo += acuerdo_fila

    Po = sumatoria_acuerdo / N

    # 4. Cálculo de Gwet AC1
    p1 = total_unos / (N * K)
    p0 = total_ceros / (N * K)
    Pe_gwet = 2.0 * p1 * p0
    gwet_ac1 = (Po - Pe_gwet) / (1.0 - Pe_gwet) if (1.0 - Pe_gwet) != 0 else 1.0

    # 5. Cálculo de Alfa de Krippendorff
    Do = 1.0 - Po
    T = N * K
    De = (2.0 * total_ceros * total_unos) / (T * (T - 1)) if T > 1 else 0.0
    kripp_alpha = 1.0 - (Do / De) if De != 0 else 1.0

    return {
        "id": modelo_id,
        "nombre": nombre_modelo,
        "historias": total_historias,
        "emr_acuerdos": acuerdos_exactos_historia,
        "emr_pct": emr_paciente,
        "unidades_totales": N,
        "filas_111": filas_111,
        "filas_000": filas_000,
        "filas_desacuerdo": filas_desacuerdo,
        "Po": Po,
        "Gwet_AC1": gwet_ac1,
        "Krippendorff_Alpha": kripp_alpha
    }


def main():
    codigos_cif = obtener_codigos_core_set(MODELOS)

    print("=" * 95)
    print(" 🔬 EVALUACIÓN FORMAL DE REPRODUCIBILIDAD Y CONFIABILIDAD INTER-ITERACIONES (K = 3)")
    print(f"    Espacio Ontológico: 114 historias x {len(codigos_cif)} códigos CIF = {114*len(codigos_cif)} decisiones binarias")
    print("=" * 95)
    print(f" {'Modelo LLM Evaluado':<36} | {'Exact Match':<11} | {'Acuerdo Po':<11} | {'Gwet AC1':<10} | {'Kripp. α':<10}")
    print("-" * 95)

    resultados = {}
    for m in MODELOS:
        if not m["archivo"].exists():
            print(f" [ERROR] No se encuentra el archivo: {m['archivo']}")
            continue

        res = analizar_confiabilidad_modelo(m["archivo"], m["nombre"], codigos_cif, m["id"])
        resultados[m["id"]] = res
        print(f" {res['nombre']:<36} | {res['emr_acuerdos']:>3}/{res['historias']:<3} ({res['emr_pct']:>5.2f}%) | {res['Po']*100:>9.4f}% | {res['Gwet_AC1']:>10.4f} | {res['Krippendorff_Alpha']:>10.4f}")

    print("=" * 95)

    ruta_json = LLM_DIR / "resumen_fiabilidad.json"
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"💾 Resumen de fiabilidad guardado en: {ruta_json}")


if __name__ == "__main__":
    main()
