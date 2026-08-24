# -*- coding: utf-8 -*-
"""
===============================================================================
CÁLCULO DEL ACUERDO EXACTO A NIVEL DE HISTORIA CLÍNICA (REPRODUCIBILIDAD 3/3)
===============================================================================

¿Qué calcula este script?
-------------------------
Para cada uno de los 3 modelos LLM evaluados, este script revisa una por una 
las 114 historias clínicas y comprueba si las 3 iteraciones (pasadas) dieron 
EXACTAMENTE el mismo conjunto de códigos CIF.

Criterio estricto:
- Acuerdo (1): Las 3 iteraciones tienen los mismos códigos, sin faltar ni sobrar ninguno.
- No acuerdo (0): Si en alguna iteración falta un código, sobra un código o cambia uno.

Archivos analizados:
- Gemma-4-31B-it: 2026-08-11_gemma-4-31b-it-codified.json
- Gemini Flash 3.5: 2026-08-18_gemini-flash-3.5_codified.json
- Gemini Flash 3.6: 2026-08-18_gemini-flash-3.6_codified.json
"""

import json
from pathlib import Path

# 1. Rutas a los 3 archivos
BASE_DIR = Path(__file__).resolve().parents[2]
LLM_DIR = BASE_DIR / "results" / "llm_text"

MODELOS = [
    {
        "nombre": "Gemma-4-31B-it",
        "archivo": LLM_DIR / "2026-08-11_gemma-4-31b-it-codified.json"
    },
    {
        "nombre": "Gemini Flash 3.5",
        "archivo": LLM_DIR / "2026-08-18_gemini-flash-3.5_codified.json"
    },
    {
        "nombre": "Gemini Flash 3.6",
        "archivo": LLM_DIR / "2026-08-18_gemini-flash-3.6_codified.json"
    }
]


def calcular_acuerdo_modelo(ruta_archivo: Path, nombre_modelo: str):
    """Calcula el acuerdo exacto para un archivo JSON."""
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        historias = json.load(f)

    total_historias = len(historias)
    acuerdos_exactos = 0
    discrepancias = []

    for i, historia in enumerate(historias, start=1):
        # Convertimos a sets para comparar los códigos sin importar el orden
        codigos_it1 = set(historia.get("predicted_icf_it1", []))
        codigos_it2 = set(historia.get("predicted_icf_it2", []))
        codigos_it3 = set(historia.get("predicted_icf_it3", []))

        # Criterio estricto: ¿los 3 conjuntos son 100% idénticos?
        if codigos_it1 == codigos_it2 == codigos_it3:
            acuerdos_exactos += 1
        else:
            discrepancias.append({
                "historia_num": i,
                "it1": sorted(list(codigos_it1)),
                "it2": sorted(list(codigos_it2)),
                "it3": sorted(list(codigos_it3))
            })

    porcentaje = (acuerdos_exactos / total_historias) * 100.0

    return {
        "nombre": nombre_modelo,
        "total": total_historias,
        "acuerdos": acuerdos_exactos,
        "no_acuerdos": total_historias - acuerdos_exactos,
        "porcentaje": porcentaje,
        "discrepancias": discrepancias
    }


def main():
    print("=" * 80)
    print(" 📊 RESULTADOS DE ACUERDO EXACTO INTER-ITERACIONES (3/3)")
    print("=" * 80)
    print(f" {'Modelo LLM Evaluado':<38} | {'Acuerdos':<10} | {'Total':<6} | {'Porcentaje':<12}")
    print("-" * 80)

    todos_los_resultados = []

    for m in MODELOS:
        if not m["archivo"].exists():
            print(f" [ERROR] No se encuentra el archivo: {m['archivo']}")
            continue

        res = calcular_acuerdo_modelo(m["archivo"], m["nombre"])
        todos_los_resultados.append(res)
        print(f" {res['nombre']:<38} | {res['acuerdos']:>4}/{res['total']:<4} | {res['total']:<6} | {res['porcentaje']:>6.2f}%")

    print("=" * 80)
    print("\n🔍 DETALLE DE DISCREPANCIAS ENCONTRADAS:\n")

    for res in todos_los_resultados:
        print(f"▶ {res['nombre']}:")
        if not res["discrepancias"]:
            print("   ✅ ¡Acuerdo 100% perfecto en todas las historias! (0 discrepancias)")
        else:
            print(f"   ⚠️ Se encontraron {len(res['discrepancias'])} historias con alguna diferencia:")
            for d in res["discrepancias"]:
                print(f"      - Historia #{d['historia_num']}:")
                print(f"          * Iteración 1: {d['it1']}")
                print(f"          * Iteración 2: {d['it2']}")
                print(f"          * Iteración 3: {d['it3']}")
        print()


if __name__ == "__main__":
    main()
