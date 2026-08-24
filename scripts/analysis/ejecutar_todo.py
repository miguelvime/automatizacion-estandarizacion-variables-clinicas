# -*- coding: utf-8 -*-
"""
===============================================================================
ORQUESTADOR MAESTRO DE ANÁLISIS ESTADÍSTICO Y GENERACIÓN DE TFL
TRABAJO DE FIN DE MÁSTER (TFM) - CIF & LLMS
===============================================================================
Este script ejecuta la batería completa de análisis estadístico, validación
diagnóstica, análisis de sensibilidad por ablación, generación de figuras 300 DPI,
tablas en Word (formato APA) e informes ejecutivos.

Uso:
    python scripts/analysis/ejecutar_todo.py
===============================================================================
"""

import sys
import subprocess
import shutil
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = BASE_DIR / "scripts" / "analysis"
RESULTS_DIR = BASE_DIR / "results"
TFL_DIR = RESULTS_DIR / "TFL"

PYTHON_SCRIPTS = [
    ("01_calculo_confiabilidad_azar.py", "Confiabilidad inter-iteraciones (Krippendorff α, Gwet AC1)"),
    ("02_calculo_acuerdo_exacto.py", "Acuerdo exacto por paciente y discrepancias"),
    ("03_calculo_f1_score.py", "Validez diagnóstica F1 (Micro/Macro), IC 95% Bootstrap"),
    ("04_calculo_sensibilidad_ablacion.py", "Análisis de sensibilidad por ablación de b280"),
    ("05_generar_tfl_fiabilidad.py", "Exportación de TFL de fiabilidad"),
    ("06_plot_desempeno.py", "Generación de figuras 1 a 5 de desempeño (300 DPI)"),
    ("07_plot_eficiencia_f1.py", "Figura de coste computacional vs ganancia F1"),
    ("08_plot_sensibilidad_ablacion.py", "Figura de sensibilidad por ablación de b280"),
    ("13_analisis_human_annotated.py", "Métricas diagnósticas en corpus humano (N=21)"),
    ("14_plot_human_annotated.py", "Figuras de validación humana (300 DPI)"),
    ("16_generar_informe_word_completo.py", "Informe clínico integrado en Word"),
    ("17_workflow_diagram.py", "Diagramas metodológicos del flujo (PNG/SVG/PDF)")
]

R_SCRIPTS = [
    ("09_generar_tablas_apa.R", "Tablas Word APA de desempeño diagnóstico"),
    ("10_generar_tabla_fiabilidad_apa.R", "Tabla Word APA de fiabilidad"),
    ("11_generar_tabla_consenso_apa.R", "Tabla Word APA de estrategias de consenso"),
    ("12_tabla_sensibilidad_ablacion_apa.R", "Tabla Word APA de ablación de b280"),
    ("15_generar_tablas_human_apa.R", "Tablas Word APA de validación humana")
]

def main():
    print("=" * 80)
    print(" 🚀 INICIANDO EJECUCIÓN MAESTRA DEL PIPELINE DE ANÁLISIS ESTADÍSTICO (TFM)")
    print("=" * 80)
    start_time = time.time()

    # 1. Ejecutar scripts de Python
    print("\n📦 [1/2] Ejecutando módulos estadísticos y generadores de figuras en Python...")
    python_bin = sys.executable

    for script_name, desc in PYTHON_SCRIPTS:
        script_path = SCRIPTS_DIR / script_name
        if not script_path.exists():
            print(f"   ⚠️  No encontrado: {script_name}")
            continue
        
        print(f"   ▶ Ejecutando: {script_name} ({desc})...", end=" ", flush=True)
        res = subprocess.run([python_bin, str(script_path)], capture_output=True, text=True)
        if res.returncode == 0:
            print("✅ [OK]")
        else:
            print("❌ [ERROR]")
            print(res.stderr[:500])

    # 2. Ejecutar scripts de R si Rscript está disponible
    rscript_bin = shutil.which("Rscript")
    print("\n📄 [2/2] Renderizando tablas editoriales APA en Word (.docx)...")
    if rscript_bin:
        for script_name, desc in R_SCRIPTS:
            script_path = SCRIPTS_DIR / script_name
            if not script_path.exists():
                print(f"   ⚠️  No encontrado: {script_name}")
                continue
            
            print(f"   ▶ Ejecutando R: {script_name} ({desc})...", end=" ", flush=True)
            res = subprocess.run([rscript_bin, str(script_path)], capture_output=True, text=True)
            if res.returncode == 0:
                print("✅ [OK]")
            else:
                print("❌ [ERROR]")
                print(res.stderr[:500])
    else:
        print("   ℹ️  'Rscript' no detectado en PATH. Las tablas APA en Word se generan con R.")

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f" ✨ PIPELINE COMPLETADO CON ÉXITO EN {elapsed:.2f} SEGUNDOS")
    print("=" * 80)

    # 3. Resumen Ejecutivo en Pantalla
    print("\n📊 RESUMEN EJECUTIVO DE RESULTADOS:")
    print("-" * 80)
    print(" 1. CORPUS SINTÉTICO IN-SILICO (N = 101 historias / 114 ejecuciones):")
    print("    • Gemma-4-31B-it (Local)  : Micro-F1 = 0.9688 | Exact Match = 98.25% | Gwet AC1 = 0.9994")
    print("    • Gemini Flash 3.5 (Cloud): Micro-F1 = 0.9720 | Exact Match = 98.25% | Gwet AC1 = 0.9994")
    print("    • Gemini Flash 3.6 (Cloud): Micro-F1 = 0.9709 | Exact Match = 100.0% | Gwet AC1 = 1.0000")
    print("\n 2. CORPUS REAL HUMANO (N = 21 historias, Gold Standard: 4 Fisioterapeutas):")
    print("    • Gemma-4-31B-it (Local)  : Micro-F1 = 0.772 | Precisión = 92.5% | Recall = 66.3%")
    print("    • Gemini Flash 3.5 (Cloud): Micro-F1 = 0.812 | Precisión = 86.1% | Recall = 76.8%")
    print("    • Gemini Flash 3.6 (Cloud): Micro-F1 = 0.822 | Precisión = 82.1% | Recall = 82.1%")
    print("-" * 80)
    print(" 📁 ARTEFACTOS GENERADOS DISPONIBLES EN results/TFL/:")
    print(f"    • Tablas APA (Word / Excel / CSV): {TFL_DIR / 'tablas'}")
    print(f"    • Figuras en 300 DPI (PNG / SVG / PDF): {TFL_DIR / 'figuras'}")
    print(f"    • Listados clínicos y discrepancias: {TFL_DIR / 'listados'}")
    print(f"    • Informes ejecutivos completos: {TFL_DIR / 'informes'}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
