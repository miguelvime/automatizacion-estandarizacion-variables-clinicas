# -*- coding: utf-8 -*-
import json
from pathlib import Path

p = Path('/home/miguelvime/projects/2026-03-11_TFM/results/human_text/resumen_human_annotated.json')
d = json.loads(p.read_text(encoding='utf-8'))

for k, name in [('gemma_31b', 'Gemma-4-31B-it (Local)'), ('flash_35', 'Gemini Flash 3.5'), ('flash_36', 'Gemini Flash 3.6')]:
    m = d[k]
    f = m['fiabilidad']
    dp = m['desempeno']
    ci = m['ci_95']
    print(f"Model: {name}")
    print(f"   Fiabilidad: Exact Match={f['exact_iter_n']}/{f['n_historias']} ({f['pae_pct']:.2f}%), Po={f['Po']:.4f}, AC1={f['ac1']:.4f}, Alpha={f['alpha']:.4f}")
    print(f"   Desempeño:  Micro-F1={dp['micro']['f1']:.4f} [IC 95%: {ci['micro'][0]:.4f} - {ci['micro'][1]:.4f}], Precisión={dp['micro']['p']:.4f}, Recall={dp['micro']['r']:.4f}")
    print(f"   Macro/Wght: Macro-F1={dp['macro']['f1']:.4f} [IC 95%: {ci['macro'][0]:.4f} - {ci['macro'][1]:.4f}], Weighted-F1={dp['weighted']['f1']:.4f} [IC 95%: {ci['weighted'][0]:.4f} - {ci['weighted'][1]:.4f}]")
    print(f"   Matriz Conf: TP={dp['tp']}, FP={dp['fp']}, FN={dp['fn']}, EMR={dp['exact']}/{dp['n']} ({dp['emr']:.2f}%)")
    print()
