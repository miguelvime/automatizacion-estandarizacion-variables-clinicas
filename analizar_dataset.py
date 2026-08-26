# -*- coding: utf-8 -*-
"""
===============================================================================
ANALIZADOR UNIVERSAL DE DATASETS CIF (N8N / LLM PIPELINE)
===============================================================================
Script universal de 1 solo paso para analizar cualquier archivo JSON codificado
por el flujo de n8n.

Detección automática:
- Si el archivo contiene Ground Truth ('icf_codes') -> Modo Evaluación (F1, Precisión, Recall)
- Si el archivo solo contiene textos y predicciones -> Modo Clínico (Prevalencia, Frecuencias, Acuerdo 3/3)

Uso:
    python analizar_dataset.py [ruta/archivo_codificado.json] [--nombre "Nombre del Estudio"]

Ejemplos:
    python analizar_dataset.py data/test_data/test_codifier_output.json
    python analizar_dataset.py results/human_text/human_annotated_flash-3.6.json --nombre "Cohorte Fisioterapia 2026"
===============================================================================
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
TFL_DIR = RESULTS_DIR / "TFL"
INFORMES_DIR = TFL_DIR / "informes"

ICF_DESCRIPTIONS = {
    "b130": "Funciones de la energía y los impulsos",
    "b134": "Funciones del sueño",
    "b147": "Funciones psicomotoras",
    "b152": "Funciones emocionales",
    "b1602": "Contenido del pensamiento",
    "b1801": "Sensación de dolor generalizado",
    "b280": "Sensación de dolor",
    "b28010": "Dolor en la cabeza y cuello",
    "b28011": "Dolor en el pecho",
    "b28013": "Dolor en la espalda",
    "b28014": "Dolor en extremidades superiores",
    "b28015": "Dolor en extremidades inferiores",
    "b455": "Tolerancia al ejercicio físico",
    "b710": "Movilidad articular",
    "b730": "Fuerza muscular",
    "b740": "Resistencia muscular",
    "b760": "Control de movimientos voluntarios",
    "d175": "Resolver problemas",
    "d230": "Llevar a cabo rutinas diarias",
    "d240": "Manejo del estrés y demandas psicológicas",
    "d410": "Cambiar posturas corporales básicas",
    "d415": "Mantener posición del cuerpo",
    "d430": "Levantar y llevar objetos",
    "d450": "Andar y desplazarse",
    "d455": "Desplazarse por el entorno",
    "d640": "Quehaceres de la casa",
    "d760": "Relaciones familiares",
    "d770": "Relaciones interpersonales complejas",
    "d850": "Trabajo remunerado",
    "d920": "Tiempo libre y ocio",
    "e1101": "Medicamentos",
    "e310": "Familiares cercanos (apoyo social)",
    "e355": "Profesionales de la salud",
    "e410": "Actitudes de familiares",
    "e570": "Servicios de seguridad social"
}

def load_json_file(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("El archivo JSON debe contener una lista de objetos/historias clínicas.")
    return data

def analyze_dataset(data: list, dataset_name: str, file_path: Path):
    n_cases = len(data)
    if n_cases == 0:
        raise ValueError("El archivo JSON está vacío.")
    
    # 1. Detectar si tiene Ground Truth
    first_item = data[0]
    gt_key = next((k for k in ["icf_codes", "gold_standard", "true_codes", "gt_codes"] if k in first_item), None)
    has_gt = gt_key is not None
    
    pred_key = next((k for k in ["predicted_icf_codes_consensus", "predicted_codes", "icf_predicted", "codes"] if k in first_item), None)
    if not pred_key:
        pred_key = "predicted_icf_codes_consensus"
    
    # 2. Métricas de Fiabilidad Inter-Iteración (si hay it1, it2, it3)
    has_iterations = "predicted_icf_it1" in first_item and "predicted_icf_it2" in first_item and "predicted_icf_it3" in first_item
    exact_iteration_agreements = 0
    
    if has_iterations:
        for item in data:
            it1 = set(item.get("predicted_icf_it1") or [])
            it2 = set(item.get("predicted_icf_it2") or [])
            it3 = set(item.get("predicted_icf_it3") or [])
            if it1 == it2 == it3:
                exact_iteration_agreements += 1
        pct_iter_agreement = (exact_iteration_agreements / n_cases) * 100
    else:
        pct_iter_agreement = None

    # 3. Conteo de Códigos y Frecuencias
    all_predicted_codes = []
    for item in data:
        preds = item.get(pred_key) or []
        all_predicted_codes.extend(preds)
    
    code_counts = Counter(all_predicted_codes)
    total_codes_extracted = len(all_predicted_codes)
    avg_codes_per_patient = total_codes_extracted / n_cases if n_cases > 0 else 0
    
    # Capítulos CIF
    chapter_counts = {"b": 0, "d": 0, "e": 0}
    for code, count in code_counts.items():
        ch = code[0].lower()
        if ch in chapter_counts:
            chapter_counts[ch] += count
            
    # 4. Modo Evaluación si has_gt es True
    eval_metrics = None
    if has_gt:
        tp_total = 0
        fp_total = 0
        fn_total = 0
        exact_matches = 0
        
        per_code_metrics = {}
        all_possible_codes = set(all_predicted_codes)
        for item in data:
            all_possible_codes.update(item.get(gt_key) or [])
            
        for code in all_possible_codes:
            per_code_metrics[code] = {"tp": 0, "fp": 0, "fn": 0}
            
        for item in data:
            gt_set = set(item.get(gt_key) or [])
            pred_set = set(item.get(pred_key) or [])
            
            if gt_set == pred_set:
                exact_matches += 1
                
            tp = len(gt_set & pred_set)
            fp = len(pred_set - gt_set)
            fn = len(gt_set - pred_set)
            
            tp_total += tp
            fp_total += fp
            fn_total += fn
            
            for c in (gt_set & pred_set):
                per_code_metrics[c]["tp"] += 1
            for c in (pred_set - gt_set):
                per_code_metrics[c]["fp"] += 1
            for c in (gt_set - pred_set):
                per_code_metrics[c]["fn"] += 1
                
        micro_p = tp_total / (tp_total + fp_total) if (tp_total + fp_total) > 0 else 0
        micro_r = tp_total / (tp_total + fn_total) if (tp_total + fn_total) > 0 else 0
        micro_f1 = (2 * micro_p * micro_r) / (micro_p + micro_r) if (micro_p + micro_r) > 0 else 0
        emr_pct = (exact_matches / n_cases) * 100
        
        # Macro F1
        f1_list = []
        for c, m in per_code_metrics.items():
            p = m["tp"] / (m["tp"] + m["fp"]) if (m["tp"] + m["fp"]) > 0 else 0
            r = m["tp"] / (m["tp"] + m["fn"]) if (m["tp"] + m["fn"]) > 0 else 0
            f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0
            if (m["tp"] + m["fn"]) > 0:  # Solo clases con soporte
                f1_list.append(f1)
        macro_f1 = sum(f1_list) / len(f1_list) if f1_list else 0
        
        # Capítulos CIF (F1 por capítulo)
        chap_f1 = {}
        for ch in ["b", "d", "e"]:
            ch_tp = sum(m["tp"] for c, m in per_code_metrics.items() if c.startswith(ch))
            ch_fp = sum(m["fp"] for c, m in per_code_metrics.items() if c.startswith(ch))
            ch_fn = sum(m["fn"] for c, m in per_code_metrics.items() if c.startswith(ch))
            
            p = ch_tp / (ch_tp + ch_fp) if (ch_tp + ch_fp) > 0 else 0
            r = ch_tp / (ch_tp + ch_fn) if (ch_tp + ch_fn) > 0 else 0
            f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0
            chap_f1[ch] = {"f1": round(f1 * 100, 2), "p": round(p * 100, 2), "r": round(r * 100, 2)}
            
        eval_metrics = {
            "micro_f1": round(micro_f1 * 100, 2),
            "macro_f1": round(macro_f1 * 100, 2),
            "precision": round(micro_p * 100, 2),
            "recall": round(micro_r * 100, 2),
            "emr_pct": round(emr_pct, 2),
            "exact_matches": exact_matches,
            "tp_total": tp_total,
            "fp_total": fp_total,
            "fn_total": fn_total,
            "chapter_f1": chap_f1
        }
        
    return {
        "dataset_name": dataset_name,
        "file_name": file_path.name,
        "file_path": str(file_path),
        "n_cases": n_cases,
        "has_gt": has_gt,
        "gt_key": gt_key,
        "pred_key": pred_key,
        "has_iterations": has_iterations,
        "pct_iter_agreement": pct_iter_agreement,
        "total_codes_extracted": total_codes_extracted,
        "avg_codes_per_patient": round(avg_codes_per_patient, 2),
        "top_codes": code_counts.most_common(10),
        "chapter_counts": chapter_counts,
        "eval_metrics": eval_metrics,
        "raw_data": data
    }

def generate_html_report(results: dict):
    TFL_DIR.mkdir(parents=True, exist_ok=True)
    html_path = TFL_DIR / "dashboard_resumen.html"
    
    data_json = json.dumps(results, ensure_ascii=False)
    icf_desc_json = json.dumps(ICF_DESCRIPTIONS, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-900 text-slate-100">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel CIF - {results['dataset_name']}</title>
    <!-- Tailwind CSS (CDN) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js (CDN) -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @media print {{
            .no-print {{ display: none !important; }}
            body {{ background-color: #ffffff !important; color: #000000 !important; }}
            .card {{ border: 1px solid #cbd5e1 !important; box-shadow: none !important; background: #ffffff !important; }}
        }}
        .custom-scrollbar::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: #1e293b; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #475569; border-radius: 4px; }}
    </style>
</head>
<body class="min-h-full flex flex-col font-sans antialiased text-slate-200 bg-slate-950 selection:bg-indigo-500 selection:text-white">

    <!-- HEADER -->
    <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white shadow">
                    CIF
                </div>
                <div>
                    <h1 class="text-base font-bold text-white leading-tight">Panel de Métricas CIF: <span class="text-indigo-400">{results['dataset_name']}</span></h1>
                    <p class="text-[11px] text-slate-400">Archivo: {results['file_name']} &bull; N = {results['n_cases']} historias</p>
                </div>
            </div>
            <div class="flex items-center space-x-2 no-print">
                <span class="px-2.5 py-1 rounded-full text-xs font-semibold {'bg-emerald-950/80 text-emerald-400 border border-emerald-800' if results['has_gt'] else 'bg-blue-950/80 text-blue-400 border border-blue-800'}">
                    {'Modo: Validación Diagnóstica' if results['has_gt'] else 'Modo: Codificación Clínica'}
                </span>
                <button onclick="window.print()" class="px-3 py-1.5 text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg border border-slate-700 transition flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
                    Imprimir / PDF
                </button>
            </div>
        </div>
        <!-- TABS -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-2 border-t border-slate-800/60 pt-1">
            <button onclick="switchTab('overview')" id="tab-btn-overview" class="px-4 py-2 text-xs font-semibold border-b-2 border-indigo-500 text-indigo-400 transition">
                📊 Resumen Cuantitativo
            </button>
            <button onclick="switchTab('cases')" id="tab-btn-cases" class="px-4 py-2 text-xs font-medium border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition">
                📋 Visor de Historias ({results['n_cases']} casos)
            </button>
        </div>
    </header>

    <!-- MAIN CONTENT -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

        <!-- ================= TAB 1: OVERVIEW ================= -->
        <section id="tab-overview" class="space-y-6">
            
            <!-- KPIS GRID -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                
                {f'''
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow">
                    <div class="text-[11px] text-slate-400 font-medium">Micro-F1 Global</div>
                    <div class="text-2xl font-black text-emerald-400 mt-1">{results["eval_metrics"]["micro_f1"]}%</div>
                    <div class="text-[10px] text-slate-500 mt-0.5">Macro-F1: {results["eval_metrics"]["macro_f1"]}%</div>
                </div>
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow">
                    <div class="text-[11px] text-slate-400 font-medium">Precisión Diagnóstica</div>
                    <div class="text-2xl font-black text-white mt-1">{results["eval_metrics"]["precision"]}%</div>
                    <div class="text-[10px] text-slate-500 mt-0.5">Falsos Positivos: {results["eval_metrics"]["fp_total"]}</div>
                </div>
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow">
                    <div class="text-[11px] text-slate-400 font-medium">Sensibilidad (Recall)</div>
                    <div class="text-2xl font-black text-white mt-1">{results["eval_metrics"]["recall"]}%</div>
                    <div class="text-[10px] text-slate-500 mt-0.5">Falsos Negativos: {results["eval_metrics"]["fn_total"]}</div>
                </div>
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow">
                    <div class="text-[11px] text-slate-400 font-medium">Exact Match (EMR)</div>
                    <div class="text-2xl font-black text-indigo-400 mt-1">{results["eval_metrics"]["emr_pct"]}%</div>
                    <div class="text-[10px] text-slate-500 mt-0.5">{results["eval_metrics"]["exact_matches"]}/{results["n_cases"]} historias perfectas</div>
                </div>
                ''' if results['has_gt'] else f'''
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow">
                    <div class="text-[11px] text-slate-400 font-medium">Historias Procesadas</div>
                    <div class="text-2xl font-black text-white mt-1">{results["n_cases"]}</div>
                    <div class="text-[10px] text-slate-500 mt-0.5">Casos clínicos analizados</div>
                </div>
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow">
                    <div class="text-[11px] text-slate-400 font-medium">Códigos CIF Asignados</div>
                    <div class="text-2xl font-black text-indigo-400 mt-1">{results["total_codes_extracted"]}</div>
                    <div class="text-[10px] text-slate-500 mt-0.5">Media: {results["avg_codes_per_patient"]} códigos/paciente</div>
                </div>
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow">
                    <div class="text-[11px] text-slate-400 font-medium">Acuerdo Consenso (3/3)</div>
                    <div class="text-2xl font-black text-emerald-400 mt-1">{results["pct_iter_agreement"]:.1f}%</div>
                    <div class="text-[10px] text-slate-500 mt-0.5">Coincidencia inter-iteración</div>
                </div>
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow">
                    <div class="text-[11px] text-slate-400 font-medium">Capítulo Dominante</div>
                    <div class="text-2xl font-black text-amber-400 mt-1">Funciones (b)</div>
                    <div class="text-[10px] text-slate-500 mt-0.5">{results["chapter_counts"]["b"]} menciones</div>
                </div>
                '''}

            </div>

            <!-- CHARTS GRID -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                <!-- CHART 1: TOP CODES OR CHAPTERS -->
                <div class="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow">
                    <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Distribución por Capítulos CIF</h3>
                    <div class="h-60">
                        <canvas id="chartChapters"></canvas>
                    </div>
                </div>

                <!-- CHART 2: FREQUENT CODES -->
                <div class="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow">
                    <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Top 10 Códigos CIF Más Frecuentes</h3>
                    <div class="h-60">
                        <canvas id="chartTopCodes"></canvas>
                    </div>
                </div>

            </div>

        </section>

        <!-- ================= TAB 2: CASES AUDIT ================= -->
        <section id="tab-cases" class="hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                <!-- LIST OF CASES -->
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow flex flex-col h-[560px]">
                    <div class="mb-3 flex items-center justify-between">
                        <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400">Historias Clínicas</h3>
                        <span class="text-[10px] text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-900">{results['n_cases']} casos</span>
                    </div>
                    <div id="case-list-container" class="flex-1 overflow-y-auto space-y-2 pr-1 custom-scrollbar">
                        <!-- Injected via JS -->
                    </div>
                </div>

                <!-- CASE DETAIL -->
                <div class="lg:col-span-2 p-5 rounded-xl bg-slate-900 border border-slate-800 shadow flex flex-col h-[560px] overflow-y-auto custom-scrollbar space-y-4">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                        <div>
                            <span id="detail-case-badge" class="text-xs font-bold px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800">Caso #--</span>
                        </div>
                        <div id="detail-case-match-status" class="text-xs font-bold px-2.5 py-1 rounded-md border">
                            --
                        </div>
                    </div>

                    <!-- TEXT -->
                    <div>
                        <div class="text-xs font-bold text-slate-400 mb-1">Texto Clínico:</div>
                        <div id="detail-clinical-text" class="p-3.5 rounded-lg bg-slate-950 text-slate-300 text-xs leading-relaxed border border-slate-800">
                            <!-- Injected via JS -->
                        </div>
                    </div>

                    <!-- COMPARISON CODES -->
                    <div class="grid grid-cols-1 {'md:grid-cols-2' if results['has_gt'] else ''} gap-4">
                        {'''
                        <div class="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                            <div class="text-xs font-bold text-indigo-300 mb-2 flex items-center justify-between">
                                <span>Gold Standard (Referencia):</span>
                                <span id="detail-gt-count" class="text-[10px] bg-indigo-950 px-1.5 py-0.5 rounded text-indigo-300 border border-indigo-800">--</span>
                            </div>
                            <div id="detail-gt-codes" class="flex flex-wrap gap-1.5"></div>
                        </div>
                        ''' if results['has_gt'] else ''}

                        <div class="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                            <div class="text-xs font-bold text-emerald-300 mb-2 flex items-center justify-between">
                                <span>Códigos Asignados (Consenso 3/3):</span>
                                <span id="detail-pred-count" class="text-[10px] bg-emerald-950 px-1.5 py-0.5 rounded text-emerald-300 border border-emerald-800">--</span>
                            </div>
                            <div id="detail-pred-codes" class="flex flex-wrap gap-1.5"></div>
                        </div>
                    </div>

                    {'''
                    <!-- DIAGNOSTIC AUDIT BADGES -->
                    <div class="p-3 rounded-lg bg-slate-950/50 border border-slate-800/60 text-xs space-y-1.5 text-slate-400">
                        <div class="font-bold text-slate-300 text-[11px]">Resumen de Clasificación:</div>
                        <div id="detail-audit-badges" class="flex flex-wrap gap-2 text-[11px]"></div>
                    </div>
                    ''' if results['has_gt'] else ''}

                </div>

            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="border-t border-slate-800 bg-slate-950 py-3 text-center text-xs text-slate-500 no-print">
        <p>Pipeline de Codificación y Validación CIF &bull; Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </footer>

    <!-- JAVASCRIPT LOGIC -->
    <script>
        const RESULTS = {data_json};
        const ICF_DESCRIPTIONS = {icf_desc_json};
        let selectedCaseIndex = 0;
        let chartChaptersInstance = null;
        let chartTopCodesInstance = null;

        function switchTab(tabId) {{
            ['overview', 'cases'].forEach(t => {{
                document.getElementById('tab-' + t).classList.add('hidden');
                document.getElementById('tab-btn-' + t).className = 'px-4 py-2 text-xs font-medium border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition';
            }});
            document.getElementById('tab-' + tabId).classList.remove('hidden');
            document.getElementById('tab-btn-' + tabId).className = 'px-4 py-2 text-xs font-semibold border-b-2 border-indigo-500 text-indigo-400 transition';
            
            if (tabId === 'overview') {{
                setTimeout(renderCharts, 50);
            }}
        }}

        function renderCharts() {{
            // CHART 1: Chapters
            const ctx1 = document.getElementById('chartChapters').getContext('2d');
            if (chartChaptersInstance) chartChaptersInstance.destroy();

            const chData = RESULTS.has_gt 
                ? [RESULTS.eval_metrics.chapter_f1.b.f1, RESULTS.eval_metrics.chapter_f1.d.f1, RESULTS.eval_metrics.chapter_f1.e.f1]
                : [RESULTS.chapter_counts.b, RESULTS.chapter_counts.d, RESULTS.chapter_counts.e];

            const labelTitle = RESULTS.has_gt ? 'F1-Score por Capítulo (%)' : 'Total Menciones Asignadas';

            chartChaptersInstance = new Chart(ctx1, {{
                type: 'bar',
                data: {{
                    labels: ['Funciones Corporales (b)', 'Actividades / Part. (d)', 'Factores Amb. (e)'],
                    datasets: [{{
                        label: labelTitle,
                        data: chData,
                        backgroundColor: ['rgba(99, 102, 241, 0.85)', 'rgba(16, 185, 129, 0.85)', 'rgba(245, 158, 11, 0.85)'],
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});

            // CHART 2: Top Codes
            const ctx2 = document.getElementById('chartTopCodes').getContext('2d');
            if (chartTopCodesInstance) chartTopCodesInstance.destroy();

            const topLabels = RESULTS.top_codes.map(x => x[0]);
            const topCounts = RESULTS.top_codes.map(x => x[1]);

            chartTopCodesInstance = new Chart(ctx2, {{
                type: 'bar',
                data: {{
                    labels: topLabels,
                    datasets: [{{
                        label: 'Frecuencia de Aparición',
                        data: topCounts,
                        backgroundColor: 'rgba(99, 102, 241, 0.75)',
                        borderColor: '#6366f1',
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});
        }}

        function renderCasesList() {{
            const container = document.getElementById('case-list-container');
            container.innerHTML = '';

            RESULTS.raw_data.forEach((c, idx) => {{
                const gt = RESULTS.has_gt ? (c[RESULTS.gt_key] || []) : [];
                const pred = c[RESULTS.pred_key] || [];
                const isExact = RESULTS.has_gt ? (gt.length === pred.length && gt.every(code => pred.includes(code))) : true;
                
                const btn = document.createElement('button');
                btn.className = `w-full text-left p-2.5 rounded-lg border transition flex items-center justify-between ${{
                    idx === selectedCaseIndex 
                        ? 'bg-indigo-950/80 border-indigo-500 text-white' 
                        : 'bg-slate-950/50 border-slate-800 text-slate-300 hover:bg-slate-800/60'
                }}`;
                btn.onclick = () => showCaseDetail(idx);

                btn.innerHTML = `
                    <div>
                        <div class="text-xs font-bold">Caso #${{c.id_clinical_text || (idx+1)}}</div>
                        <div class="text-[11px] text-slate-400 truncate w-44 mt-0.5">${{(c.clinical_text || '').substring(0, 45)}}...</div>
                    </div>
                    <span class="text-[10px] font-bold px-1.5 py-0.5 rounded ${{
                        RESULTS.has_gt 
                            ? (isExact ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-amber-950 text-amber-400 border border-amber-800')
                            : 'bg-indigo-950 text-indigo-300 border border-indigo-800'
                    }}">
                        ${{RESULTS.has_gt ? (isExact ? 'Exacto' : 'Discrep.') : `${{pred.length}} Códigos`}}
                    </span>
                `;
                container.appendChild(btn);
            }});
        }}

        function showCaseDetail(idx) {{
            selectedCaseIndex = idx;
            renderCasesList();

            const c = RESULTS.raw_data[idx];
            if (!c) return;

            document.getElementById('detail-case-badge').innerText = `Caso #${{c.id_clinical_text || (idx+1)}}`;
            document.getElementById('detail-clinical-text').innerText = `“${{c.clinical_text || 'Sin texto registrado'}}”`;

            const gt = RESULTS.has_gt ? (c[RESULTS.gt_key] || []) : [];
            const pred = c[RESULTS.pred_key] || [];

            const isExact = RESULTS.has_gt ? (gt.length === pred.length && gt.every(code => pred.includes(code))) : true;
            const statusBadge = document.getElementById('detail-case-match-status');
            
            if (RESULTS.has_gt) {{
                if (isExact) {{
                    statusBadge.className = 'text-xs font-bold text-emerald-400 bg-emerald-950/80 px-2.5 py-0.5 rounded border border-emerald-800';
                    statusBadge.innerText = '✓ Coincidencia Exacta';
                }} else {{
                    statusBadge.className = 'text-xs font-bold text-amber-400 bg-amber-950/80 px-2.5 py-0.5 rounded border border-amber-800';
                    statusBadge.innerText = '⚠️ Discrepancia';
                }}
                document.getElementById('detail-gt-count').innerText = `${{gt.length}} códigos`;
            }} else {{
                statusBadge.className = 'text-xs font-bold text-indigo-400 bg-indigo-950/80 px-2.5 py-0.5 rounded border border-indigo-800';
                statusBadge.innerText = `${{pred.length}} Códigos CIF Asignados`;
            }}

            document.getElementById('detail-pred-count').innerText = `${{pred.length}} códigos`;

            if (RESULTS.has_gt) {{
                const gtContainer = document.getElementById('detail-gt-codes');
                gtContainer.innerHTML = '';
                gt.forEach(code => {{
                    const desc = ICF_DESCRIPTIONS[code] || '';
                    const isHit = pred.includes(code);
                    const tag = document.createElement('span');
                    tag.className = `px-2 py-0.5 rounded text-xs font-medium flex items-center gap-1 border ${{
                        isHit ? 'bg-indigo-950/90 text-indigo-300 border-indigo-700' : 'bg-rose-950/80 text-rose-300 border-rose-800'
                    }}`;
                    tag.title = desc;
                    tag.innerHTML = `<strong>${{code}}</strong> <span class="text-[10px] text-slate-400">(${{desc}})</span>`;
                    gtContainer.appendChild(tag);
                }});
            }}

            const predContainer = document.getElementById('detail-pred-codes');
            predContainer.innerHTML = '';
            pred.forEach(code => {{
                const desc = ICF_DESCRIPTIONS[code] || '';
                const isTp = RESULTS.has_gt ? gt.includes(code) : true;
                const tag = document.createElement('span');
                tag.className = `px-2 py-0.5 rounded text-xs font-medium flex items-center gap-1 border ${{
                    isTp ? 'bg-emerald-950/90 text-emerald-300 border-emerald-700' : 'bg-amber-950/80 text-amber-300 border-amber-800'
                }}`;
                tag.title = desc;
                tag.innerHTML = `<strong>${{code}}</strong> <span class="text-[10px] text-slate-400">(${{desc}})</span>`;
                predContainer.appendChild(tag);
            }});

            if (RESULTS.has_gt) {{
                const tpList = pred.filter(code => gt.includes(code));
                const fpList = pred.filter(code => !gt.includes(code));
                const fnList = gt.filter(code => !pred.includes(code));

                const auditContainer = document.getElementById('detail-audit-badges');
                auditContainer.innerHTML = `
                    <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">Aciertos (TP): ${{tpList.length}} [${{tpList.join(', ') || 'ninguno'}}]</span>
                    <span class="px-2 py-0.5 rounded bg-amber-950 text-amber-400 border border-amber-800">Falsos Positivos (FP): ${{fpList.length}} [${{fpList.join(', ') || 'ninguno'}}]</span>
                    <span class="px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800">Falsos Negativos (FN): ${{fnList.length}} [${{fnList.join(', ') || 'ninguno'}}]</span>
                `;
            }}
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            renderCharts();
            renderCasesList();
            showCaseDetail(0);
        }});
    </script>
</body>
</html>
"""
    html_path.write_text(html, encoding="utf-8")
    return html_path

def generate_markdown_summary(results: dict):
    INFORMES_DIR.mkdir(parents=True, exist_ok=True)
    report_path = INFORMES_DIR / "INFORME_EJECUTIVO_METRICAS.md"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    if results['has_gt']:
        m = results['eval_metrics']
        md = f"""# 📊 Informe de Evaluación Diagnóstica CIF
**Dataset:** {results['dataset_name']} ({results['file_name']})  
**Fecha:** {date_str}  
**Muestra:** N = {results['n_cases']} historias clínicas

---

## 🎯 Métricas Globales
* **Micro-F1:** **{m['micro_f1']}%**
* **Macro-F1:** {m['macro_f1']}%
* **Exact Match (EMR):** {m['emr_pct']}% ({m['exact_matches']}/{results['n_cases']} aciertos totales)
* **Precisión:** {m['precision']}% (Falsos Positivos = {m['fp_total']})
* **Sensibilidad (Recall):** {m['recall']}% (Falsos Negativos = {m['fn_total']})

---

## 🔍 Desglose por Capítulos CIF
* **Funciones Corporales (`b`):** F1 = {m['chapter_f1']['b']['f1']}% | Precisión = {m['chapter_f1']['b']['p']}% | Recall = {m['chapter_f1']['b']['r']}%
* **Actividades y Participación (`d`):** F1 = {m['chapter_f1']['d']['f1']}% | Precisión = {m['chapter_f1']['d']['p']}% | Recall = {m['chapter_f1']['d']['r']}%
* **Factores Ambientales (`e`):** F1 = {m['chapter_f1']['e']['f1']}% | Precisión = {m['chapter_f1']['e']['p']}% | Recall = {m['chapter_f1']['e']['r']}%
"""
    else:
        md = f"""# 📊 Resumen de Codificación Clínica CIF
**Dataset:** {results['dataset_name']} ({results['file_name']})  
**Fecha:** {date_str}  
**Muestra:** N = {results['n_cases']} historias clínicas

---

## 🎯 Resumen de Extracción
* **Total de historias procesadas:** {results['n_cases']}
* **Total de códigos CIF asignados:** {results['total_codes_extracted']}
* **Media de códigos por paciente:** {results['avg_codes_per_patient']}
* **Acuerdo de Consenso 3/3:** {results['pct_iter_agreement']:.1f}%

---

## 🏆 Códigos Más Frecuentes
"""
        for code, count in results['top_codes']:
            desc = ICF_DESCRIPTIONS.get(code, "Descripción no disponible")
            pct = (count / results['n_cases']) * 100
            md += f"* **{code}** ({desc}): {count} menciones ({pct:.1f}% de pacientes)\n"

    report_path.write_text(md, encoding="utf-8")
    return report_path

def main():
    parser = argparse.ArgumentParser(description="Analizador Universal de Datasets CIF")
    parser.add_argument("input_file", nargs="?", help="Ruta al archivo JSON codificado")
    parser.add_argument("--nombre", "-n", default=None, help="Nombre identificativo del dataset")
    args = parser.parse_args()

    # Si no se pasa archivo, buscar archivo predeterminado más relevante
    if not args.input_file:
        default_candidates = [
            RESULTS_DIR / "human_text" / "human_annotated_flash-3.6.json",
            RESULTS_DIR / "llm_text" / "2026-08-18_gemini-flash-3.6_codified.json",
            BASE_DIR / "data" / "test_data" / "test_codifier_output.json"
        ]
        chosen_file = next((f for f in default_candidates if f.exists()), None)
        if not chosen_file:
            print("❌ Error: No se especificó archivo de entrada y no se encontraron candidatos predeterminados.")
            sys.exit(1)
        file_path = chosen_file
    else:
        file_path = Path(args.input_file)
        if not file_path.is_absolute():
            file_path = (BASE_DIR / file_path).resolve()

    dataset_name = args.nombre or file_path.stem.replace("_", " ").title()

    print("=" * 80)
    print(f" 🚀 ANALIZANDO DATASET: {dataset_name}")
    print(f" 📂 Archivo: {file_path}")
    print("=" * 80)

    try:
        data = load_json_file(file_path)
        results = analyze_dataset(data, dataset_name, file_path)
        
        # Generar Reporte e Informe
        html_file = generate_html_report(results)
        md_file = generate_markdown_summary(results)
        
        print("\n✨ ANÁLISIS COMPLETADO:")
        print("-" * 80)
        print(f" • Modo detectado      : {'Validación con Gold Standard' if results['has_gt'] else 'Codificación Clínica (Sin Gold Standard)'}")
        print(f" • Historias analizadas: N = {results['n_cases']}")
        
        if results['has_gt']:
            m = results['eval_metrics']
            print(f" • Desempeño Global    : Micro-F1 = {m['micro_f1']}% | Precisión = {m['precision']}% | Recall = {m['recall']}%")
            print(f" • Exact Match Ratio   : {m['emr_pct']}% ({m['exact_matches']}/{results['n_cases']} historias perfectas)")
        else:
            print(f" • Códigos extraídos   : {results['total_codes_extracted']} (media: {results['avg_codes_per_patient']} / paciente)")
            if results['has_iterations']:
                print(f" • Consenso Estricto   : {results['pct_iter_agreement']:.1f}% de acuerdo total entre las 3 iteraciones")
        
        print("-" * 80)
        print(f" 📁 Dashboard Interactivo HTML : {html_file}")
        print(f" 📁 Informe Resumen Markdown   : {md_file}")
        print("=" * 80 + "\n")

    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
