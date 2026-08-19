#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workflow_diagram.py
-------------------
Generador de diagramas metodológicos claros y legibles para el Trabajo de Fin de Máster (TFM):
"Codificación automatizada de texto clínico no estructurado según la CIF mediante LLMs".

Basado directamente en los apartados de Metodología de la memoria del TFM:
1. Generación del conjunto de datos (38 combinaciones CIF -> n8n + Gemini -> 114 historias clínicas)
2. Codificación del texto clínico generado (114 historias -> n8n + LLMs [3 runs + consenso] -> Predicciones CIF)
3. Análisis de resultados (Predicciones vs Ground Truth -> Python/R -> F1, PAE, AC1 de Gwet, α de Krippendorff)

Soporta dos estilos:
- 'linear': Diagrama secuencial horizontal con tipografía grande, cajas ajustadas y máxima legibilidad (Recomendado).
- 'phases': Diagrama estructurado en 3 columnas por fases metodológicas detalladas.

Uso:
    python scripts/TFL/workflow_diagram.py [--style {phases,linear,both}] [--lang {es,en,both}] [--dpi DPI]
"""

import os
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def create_linear_diagram(output_dir="./data/results/TFL", lang="es", dpi=300):
    """
    Genera una versión lineal compacta con tipografía maximizada y cajas ajustadas sin espacio vacío.
    """
    os.makedirs(output_dir, exist_ok=True)

    content_es = {
        "title": "Pipeline Metodológico: Generación, Codificación CIF y Evaluación",
        "subtitle": "Flujo de trabajo experimental desde el diseño del Ground Truth hasta la evaluación comparativa",
        
        "b1_title": "Combinaciones CIF",
        "b1_sub": "38 combinaciones\nCore Set dolor crónico\nDominios b, s, d, e",
        "b1_tag": "GROUND TRUTH",
        "t1_title": "Flujo Generador",
        "t1_sub": "n8n + Gemini",
        
        "b2_title": "Texto Clínico",
        "b2_sub": "114 historias clínicas\nsintéticas estructuradas\n(Formato JSON)",
        "b2_tag": "CORPUS IN SILICO",
        "t2_title": "Flujo Codificador",
        "t2_sub": "n8n + LLMs (3 runs)",
        
        "b3_title": "Dataset Codificado",
        "b3_sub": "Predicciones CIF por\niteración y consenso\n(Gemini y Gemma)",
        "b3_tag": "PREDICCIONES",
        "t3_title": "Scripts Análisis",
        "t3_sub": "Python & R",
        
        "b4_title": "Evaluación",
        "b4_sub": "Validez: F1-score, PAE\nFiabilidad: AC1 Gwet\ny α de Krippendorff",
        "b4_tag": "RESULTADOS TFM"
    }

    content_en = {
        "title": "Methodological Pipeline: Generation, ICF Coding, and Evaluation",
        "subtitle": "Experimental workflow from Ground Truth design to comparative model evaluation",
        
        "b1_title": "ICF Combinations",
        "b1_sub": "38 combinations\nChronic pain Core Set\nDomains b, s, d, e",
        "b1_tag": "GROUND TRUTH",
        "t1_title": "Generator Flow",
        "t1_sub": "n8n + Gemini",
        
        "b2_title": "Clinical Text",
        "b2_sub": "114 synthetic\nclinical narratives\n(JSON Format)",
        "b2_tag": "IN SILICO CORPUS",
        "t2_title": "Codifier Flow",
        "t2_sub": "n8n + LLMs (3 runs)",
        
        "b3_title": "Coded Dataset",
        "b3_sub": "Predicted ICF codes\nby run & consensus\n(Gemini & Gemma)",
        "b3_tag": "PREDICTIONS",
        "t3_title": "Analysis Scripts",
        "t3_sub": "Python & R",
        
        "b4_title": "Evaluation",
        "b4_sub": "Validity: F1-score, PAE\nReliability: Gwet's AC1\n& Krippendorff's α",
        "b4_tag": "BENCHMARK RESULTS"
    }

    C = content_es if lang == "es" else content_en

    # Proporciones ajustadas para eliminar espacio muerto
    fig, ax = plt.subplots(figsize=(20.0, 6.2), dpi=dpi)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Fondo general
    bg_box = FancyBboxPatch((0.4, 0.4), 99.2, 99.2, boxstyle="round,pad=0.2,rounding_size=1.0",
                            facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2, zorder=0)
    ax.add_patch(bg_box)

    # Cabecera principal con tipografía grande y clara
    ax.text(50, 93.0, C["title"], fontsize=19, weight='bold', color="#0F172A", ha='center', va='center')
    ax.text(50, 86.0, C["subtitle"], fontsize=12.5, style='italic', color="#475569", ha='center', va='center')
    ax.plot([10, 90], [82.0, 82.0], color="#CBD5E1", linewidth=1.0)

    boxes = [
        {"title": C["b1_title"], "sub": C["b1_sub"], "tag": C["b1_tag"], "xc": 12.0, "c_border": "#0284C7", "c_hdr": "#E0F2FE", "c_tag": "#0369A1"},
        {"title": C["b2_title"], "sub": C["b2_sub"], "tag": C["b2_tag"], "xc": 37.3, "c_border": "#0D9488", "c_hdr": "#CCFBF1", "c_tag": "#0F766E"},
        {"title": C["b3_title"], "sub": C["b3_sub"], "tag": C["b3_tag"], "xc": 62.7, "c_border": "#7C3AED", "c_hdr": "#EDE9FE", "c_tag": "#6D28D9"},
        {"title": C["b4_title"], "sub": C["b4_sub"], "tag": C["b4_tag"], "xc": 88.0, "c_border": "#059669", "c_hdr": "#D1FAE5", "c_tag": "#047857"},
    ]

    transitions = [
        {"title": C["t1_title"], "sub": C["t1_sub"], "border": "#2563EB", "bg": "#EFF6FF"},
        {"title": C["t2_title"], "sub": C["t2_sub"], "border": "#7C3AED", "bg": "#F5F3FF"},
        {"title": C["t3_title"], "sub": C["t3_sub"], "border": "#DC2626", "bg": "#FEF2F2"}
    ]

    # Altura ajustada para que el contenido llene la caja de forma armónica
    bw, bh = 16.5, 52.0
    by0 = 17.0

    for b in boxes:
        xc = b["xc"]
        bx0 = xc - bw/2
        
        # Sombra suave
        shadow = FancyBboxPatch((bx0 + 0.4, by0 - 0.5), bw, bh,
                                boxstyle="round,pad=0.2,rounding_size=0.7",
                                facecolor="#E2E8F0", edgecolor="none", zorder=1)
        ax.add_patch(shadow)

        # Caja principal
        box = FancyBboxPatch((bx0, by0), bw, bh,
                             boxstyle="round,pad=0.2,rounding_size=0.7",
                             facecolor="#FFFFFF", edgecolor=b["c_border"], linewidth=2.0, zorder=2)
        ax.add_patch(box)

        # Cabecera coloreada
        hh = 17.5
        hy0 = by0 + bh - hh
        hdr = FancyBboxPatch((bx0, hy0), bw, hh,
                             boxstyle="round,pad=0.2,rounding_size=0.6",
                             facecolor=b["c_hdr"], edgecolor="none", zorder=3)
        ax.add_patch(hdr)

        # Etiqueta / Tag superior (Grande y destacada)
        ax.text(xc, hy0 + 11.8, b["tag"], fontsize=10.5, weight='bold', color=b["c_tag"], ha='center', va='center', zorder=4)
        
        # Título de la caja (Grande: 14.5pt)
        ax.text(xc, hy0 + 5.0, b["title"], fontsize=14.5, weight='bold', color="#0F172A", ha='center', va='center', zorder=4)
        ax.plot([bx0, bx0 + bw], [hy0, hy0], color=b["c_border"], linewidth=1.0, zorder=4)

        # Texto interior descriptivo (Grande: 13.0pt, llena perfectamente el espacio)
        ax.text(xc, by0 + (bh - hh)/2, b["sub"], fontsize=13.0, color="#1E293B",
                ha='center', va='center', linespacing=1.45, zorder=4)

    # Flechas y tarjetas flotantes de transición entre cajas
    for i in range(len(boxes) - 1):
        x1 = boxes[i]["xc"] + bw/2 + 0.4
        x2 = boxes[i+1]["xc"] - bw/2 - 0.4
        mid_x = (x1 + x2) / 2
        arrow_y = by0 + (bh - 17.5)/2 - 5.0

        # Flecha conectora
        arr = FancyArrowPatch((x1, arrow_y), (x2, arrow_y),
                              arrowstyle="-|>,head_length=5.5,head_width=3.6",
                              color="#334155", linewidth=2.2, zorder=5)
        ax.add_patch(arr)

        # Pastilla / Badge del flujo sobre la flecha
        t = transitions[i]
        pill_w = 8.2
        pill_h = 14.0
        pill_x0 = mid_x - pill_w/2
        pill_y0 = arrow_y + 4.0

        pill = FancyBboxPatch((pill_x0, pill_y0), pill_w, pill_h,
                              boxstyle="round,pad=0.15,rounding_size=0.4",
                              facecolor=t["bg"], edgecolor=t["border"], linewidth=1.3, zorder=5)
        ax.add_patch(pill)

        # Texto del flujo (Grande: 10pt y 9pt)
        ax.text(mid_x, pill_y0 + 9.2, t["title"], fontsize=10.0, weight='bold',
                color="#0F172A", ha='center', va='center', zorder=6)
        ax.text(mid_x, pill_y0 + 4.2, t["sub"], fontsize=9.0,
                color="#475569", ha='center', va='center', zorder=6)

    # Guardado en PNG, PDF y SVG
    png_path = os.path.join(output_dir, f"workflow_linear_{lang}.png")
    pdf_path = os.path.join(output_dir, f"workflow_linear_{lang}.pdf")
    svg_path = os.path.join(output_dir, f"workflow_linear_{lang}.svg")

    plt.tight_layout()
    fig.savefig(png_path, dpi=dpi, bbox_inches='tight', pad_inches=0.1)
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.1)
    fig.savefig(svg_path, format='svg', bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

    print(f"[{lang.upper()} - Lineal] Guardado con tipografía maximizada:")
    print(f"  - {png_path} ({dpi} DPI)")
    print(f"  - {pdf_path} (PDF)")
    print(f"  - {svg_path} (SVG)")
    return png_path


def create_phases_diagram(output_dir="./data/results/TFL", lang="es", dpi=300):
    """
    Genera el diagrama estructurado en las 3 fases clave de la metodología del TFM.
    """
    os.makedirs(output_dir, exist_ok=True)

    content_es = {
        "title": "Metodología del Trabajo Fin de Máster",
        "subtitle": "Flujo de trabajo para la generación in silico, codificación automatizada según la CIF y evaluación de LLMs",
        
        "f1_tag": "1. GENERACIÓN DEL DATASET",
        "f1_in_label": "ENTRADA",
        "f1_in_text": "Combinaciones de códigos CIF\n• 38 combinaciones (Core Set dolor crónico)\n• Ground Truth estructurado (b, s, d, e)",
        "f1_proc_label": "FLUJO GENERADOR (n8n + Gemini)",
        "f1_proc_text": "Generación in silico automatizada\n• Prompting médico con Self-Verification\n• 3 historias clínicas por combinación",
        "f1_out_label": "SALIDA",
        "f1_out_text": "114 Historias clínicas sintéticas\n• Texto libre médico estructurado en JSON",

        "f2_tag": "2. CODIFICACIÓN AUTOMATIZADA",
        "f2_in_label": "ENTRADA",
        "f2_in_text": "Texto clínico no estructurado\n• 114 historias clínicas (ciego, sin etiquetas)",
        "f2_proc_label": "FLUJO CODIFICADOR (n8n + LLMs)",
        "f2_proc_text": "Codificación automatizada\n• Inferencia con Gemini y Gemma\n• 3 iteraciones por caso + consenso",
        "f2_out_label": "SALIDA",
        "f2_out_text": "Texto clínico codificado\n• Códigos CIF predichos por iteración y consenso",

        "f3_tag": "3. ANÁLISIS DE RESULTADOS",
        "f3_in_label": "ENTRADA",
        "f3_in_text": "Predicciones vs Ground Truth\n• Matrices de códigos reales y predichos",
        "f3_proc_label": "SCRIPTS DE ANÁLISIS (Python & R)",
        "f3_proc_text": "Evaluación estadística\n• Binarización multietiqueta y prevalencia\n• Bootstrapping para intervalos de confianza",
        "f3_out_label": "SALIDA",
        "f3_out_text": "Resultados y comparativa\n• Validez: F1-score (Micro/Macro), PAE\n• Fiabilidad: AC1 de Gwet y α de Krippendorff",

        "footer": "CIF: Clasificación Internacional del Funcionamiento (OMS) • Orquestación: n8n • Modelos: Gemini-3.6-flash, Gemini-3.5-flash, Gemma-4-31b-it"
    }

    content_en = {
        "title": "Master's Thesis Methodology",
        "subtitle": "Experimental workflow for in silico generation, automated ICF coding, and LLM evaluation",
        
        "f1_tag": "1. DATASET GENERATION",
        "f1_in_label": "INPUT",
        "f1_in_text": "ICF code combinations\n• 38 combinations (chronic pain Core Set)\n• Structured Ground Truth (b, s, d, e)",
        "f1_proc_label": "GENERATOR FLOW (n8n + Gemini)",
        "f1_proc_text": "Automated in silico generation\n• Medical prompting with Self-Verification\n• 3 clinical narratives per combination",
        "f1_out_label": "OUTPUT",
        "f1_out_text": "114 Synthetic clinical narratives\n• Unstructured medical text in JSON",

        "f2_tag": "2. AUTOMATED CODING",
        "f2_in_label": "INPUT",
        "f2_in_text": "Unstructured clinical text\n• 114 clinical cases (blinded, no tags/IDs)",
        "f2_proc_label": "CODIFIER FLOW (n8n + LLMs)",
        "f2_proc_text": "Automated clinical coding\n• LLM inference (Gemini & Gemma)\n• 3 iterations per case + consensus rule",
        "f2_out_label": "OUTPUT",
        "f2_out_text": "Coded clinical dataset\n• Predicted ICF codes per run and consensus",

        "f3_tag": "3. RESULTS & BENCHMARK",
        "f3_in_label": "INPUT",
        "f3_in_text": "Predictions vs Ground Truth\n• Matrices of target vs predicted codes",
        "f3_proc_label": "ANALYSIS SCRIPTS (Python & R)",
        "f3_proc_text": "Statistical evaluation\n• MultiLabel binarization & prevalence\n• Bootstrapping for confidence intervals",
        "f3_out_label": "OUTPUT",
        "f3_out_text": "Comparative results\n• Validity: F1-score (Micro/Macro), PAE\n• Reliability: Gwet's AC1 and Krippendorff's α",

        "footer": "ICF: International Classification of Functioning (WHO) • Orchestration: n8n • Models: Gemini-3.6-flash, Gemini-3.5-flash, Gemma-4-31b-it"
    }

    C = content_es if lang == "es" else content_en

    fig, ax = plt.subplots(figsize=(16, 9.0), dpi=dpi)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    C_BG = "#F8FAFC"
    C_MAIN_TITLE = "#0F172A"
    C_SUBTITLE = "#475569"

    bg_box = FancyBboxPatch((0.5, 0.5), 99.0, 99.0, boxstyle="round,pad=0.2,rounding_size=1.0",
                            facecolor=C_BG, edgecolor="#CBD5E1", linewidth=1.2, zorder=0)
    ax.add_patch(bg_box)

    ax.text(50, 95.0, C["title"], fontsize=17, weight='bold', color=C_MAIN_TITLE, ha='center', va='center')
    ax.text(50, 91.5, C["subtitle"], fontsize=11, style='italic', color=C_SUBTITLE, ha='center', va='center')
    ax.plot([12, 88], [88.8, 88.8], color="#CBD5E1", linewidth=1.0)

    phases = [
        {
            "tag": C["f1_tag"],
            "x": 4.5, "w": 27.5,
            "border": "#0284C7", "hdr": "#E0F2FE", "tag_c": "#0369A1", "proc_bg": "#F0F9FF",
            "in_lbl": C["f1_in_label"], "in_txt": C["f1_in_text"],
            "proc_lbl": C["f1_proc_label"], "proc_txt": C["f1_proc_text"],
            "out_lbl": C["f1_out_label"], "out_txt": C["f1_out_text"],
        },
        {
            "tag": C["f2_tag"],
            "x": 36.25, "w": 27.5,
            "border": "#7C3AED", "hdr": "#EDE9FE", "tag_c": "#6D28D9", "proc_bg": "#F5F3FF",
            "in_lbl": C["f2_in_label"], "in_txt": C["f2_in_text"],
            "proc_lbl": C["f2_proc_label"], "proc_txt": C["f2_proc_text"],
            "out_lbl": C["f2_out_label"], "out_txt": C["f2_out_text"],
        },
        {
            "tag": C["f3_tag"],
            "x": 68.0, "w": 27.5,
            "border": "#059669", "hdr": "#D1FAE5", "tag_c": "#047857", "proc_bg": "#ECFDF5",
            "in_lbl": C["f3_in_label"], "in_txt": C["f3_in_text"],
            "proc_lbl": C["f3_proc_label"], "proc_txt": C["f3_proc_text"],
            "out_lbl": C["f3_out_label"], "out_txt": C["f3_out_text"],
        }
    ]

    card_y = 10.5
    card_h = 75.5

    for p in phases:
        px, pw = p["x"], p["w"]

        shadow = FancyBboxPatch((px + 0.35, card_y - 0.4), pw, card_h,
                                boxstyle="round,pad=0.2,rounding_size=0.8",
                                facecolor="#E2E8F0", edgecolor="none", zorder=1)
        ax.add_patch(shadow)

        col_box = FancyBboxPatch((px, card_y), pw, card_h,
                                 boxstyle="round,pad=0.2,rounding_size=0.8",
                                 facecolor="#FFFFFF", edgecolor=p["border"],
                                 linewidth=1.8, zorder=2)
        ax.add_patch(col_box)

        hdr_h = 7.5
        hdr_y0 = card_y + card_h - hdr_h
        hdr = FancyBboxPatch((px, hdr_y0), pw, hdr_h,
                             boxstyle="round,pad=0.2,rounding_size=0.7",
                             facecolor=p["hdr"], edgecolor="none", zorder=3)
        ax.add_patch(hdr)

        ax.text(px + pw/2, hdr_y0 + hdr_h/2, p["tag"], fontsize=10.5, weight='bold',
                color=p["tag_c"], ha='center', va='center', zorder=4)
        ax.plot([px, px + pw], [hdr_y0, hdr_y0], color=p["border"], linewidth=0.8, zorder=4)

        # 1. ENTRADA
        in_y = hdr_y0 - 19.5
        in_h = 17.5
        in_box = FancyBboxPatch((px + 1.2, in_y), pw - 2.4, in_h,
                                boxstyle="round,pad=0.1,rounding_size=0.4",
                                facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.0, zorder=3)
        ax.add_patch(in_box)
        ax.text(px + 2.2, in_y + in_h - 2.4, p["in_lbl"], fontsize=8.2, weight='bold',
                color=p["tag_c"], ha='left', va='center', zorder=4)
        ax.text(px + 2.2, in_y + in_h - 4.8, p["in_txt"], fontsize=8.6,
                color="#1E293B", ha='left', va='top', linespacing=1.35, zorder=4)

        arr1 = FancyArrowPatch((px + pw/2, in_y - 0.3), (px + pw/2, in_y - 3.2),
                               arrowstyle="-|>,head_length=4.2,head_width=2.6",
                               color=p["border"], linewidth=1.5, zorder=4)
        ax.add_patch(arr1)

        # 2. PROCESO
        proc_y = in_y - 23.0
        proc_h = 19.5
        proc_box = FancyBboxPatch((px + 1.2, proc_y), pw - 2.4, proc_h,
                                  boxstyle="round,pad=0.1,rounding_size=0.4",
                                  facecolor=p["proc_bg"], edgecolor=p["border"], linewidth=1.4, zorder=3)
        ax.add_patch(proc_box)
        ax.text(px + 2.2, proc_y + proc_h - 2.4, p["proc_lbl"], fontsize=8.2, weight='bold',
                color=p["tag_c"], ha='left', va='center', zorder=4)
        ax.text(px + 2.2, proc_y + proc_h - 4.8, p["proc_txt"], fontsize=8.6,
                color="#1E293B", ha='left', va='top', linespacing=1.35, zorder=4)

        arr2 = FancyArrowPatch((px + pw/2, proc_y - 0.3), (px + pw/2, proc_y - 3.2),
                               arrowstyle="-|>,head_length=4.2,head_width=2.6",
                               color=p["border"], linewidth=1.5, zorder=4)
        ax.add_patch(arr2)

        # 3. SALIDA
        out_y = proc_y - 21.0
        out_h = 17.5
        out_box = FancyBboxPatch((px + 1.2, out_y), pw - 2.4, out_h,
                                 boxstyle="round,pad=0.1,rounding_size=0.4",
                                 facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.0, zorder=3)
        ax.add_patch(out_box)
        ax.text(px + 2.2, out_y + out_h - 2.4, p["out_lbl"], fontsize=8.2, weight='bold',
                color=p["tag_c"], ha='left', va='center', zorder=4)
        ax.text(px + 2.2, out_y + out_h - 4.8, p["out_txt"], fontsize=8.6,
                color="#1E293B", ha='left', va='top', linespacing=1.35, zorder=4)

    # Flechas entre Fases
    arr_f1_f2 = FancyArrowPatch((32.2, card_y + card_h/2), (36.0, card_y + card_h/2),
                                arrowstyle="-|>,head_length=5.5,head_width=3.5",
                                color="#334155", linewidth=2.2, zorder=5)
    ax.add_patch(arr_f1_f2)

    arr_f2_f3 = FancyArrowPatch((64.0, card_y + card_h/2), (67.8, card_y + card_h/2),
                                arrowstyle="-|>,head_length=5.5,head_width=3.5",
                                color="#334155", linewidth=2.2, zorder=5)
    ax.add_patch(arr_f2_f3)

    # Pie de página
    footer_box = FancyBboxPatch((4.5, 3.5), 91.0, 4.8,
                                boxstyle="round,pad=0.1,rounding_size=0.3",
                                facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=0.8, zorder=2)
    ax.add_patch(footer_box)
    ax.text(50, 5.9, C["footer"], fontsize=8.0, color="#475569", ha='center', va='center', zorder=3)

    png_path = os.path.join(output_dir, f"workflow_diagram_{lang}.png")
    pdf_path = os.path.join(output_dir, f"workflow_diagram_{lang}.pdf")
    svg_path = os.path.join(output_dir, f"workflow_diagram_{lang}.svg")

    plt.tight_layout()
    fig.savefig(png_path, dpi=dpi, bbox_inches='tight', pad_inches=0.1)
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.1)
    fig.savefig(svg_path, format='svg', bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

    return png_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador del Diagrama Metodológico del TFM.")
    parser.add_argument("--output-dir", type=str, default="./data/results/TFL", help="Directorio de destino.")
    parser.add_argument("--style", type=str, choices=["phases", "linear", "both"], default="both", help="Estilo: 'phases', 'linear' o 'both'.")
    parser.add_argument("--lang", type=str, choices=["es", "en", "both"], default="both", help="Idioma: es, en o both.")
    parser.add_argument("--dpi", type=int, default=300, help="DPI para formato PNG.")

    args = parser.parse_args()

    langs = ["es", "en"] if args.lang == "both" else [args.lang]

    for l in langs:
        if args.style in ["linear", "both"]:
            create_linear_diagram(output_dir=args.output_dir, lang=l, dpi=args.dpi)
        if args.style in ["phases", "both"]:
            create_phases_diagram(output_dir=args.output_dir, lang=l, dpi=args.dpi)
