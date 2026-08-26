# -*- coding: utf-8 -*-
import json
from pathlib import Path

base_dir = Path('/home/miguelvime/projects/2026-03-11_TFM')
llm_dir = base_dir / 'results' / 'llm_text'

modelos = [
    {
        'id': 'gemma_31b',
        'nombre': 'Gemma-4-31B-it',
        'archivo': llm_dir / '2026-08-25_gemma_codified.json'
    },
    {
        'id': 'gemini_flash_35',
        'nombre': 'Gemini Flash 3.5',
        'archivo': llm_dir / '2026-08-25-flash-3.5-codified.json'
    },
    {
        'id': 'gemini_flash_37',
        'nombre': 'Gemini Flash 3.7',
        'archivo': llm_dir / '2026-08-25-3.7-flash-codified.json'
    }
]

def evaluar_estrategia(historias, get_pred_fn):
    total_tp = 0
    total_fp = 0
    total_fn = 0
    exact_matches = 0
    n = len(historias)
    
    for h in historias:
        gt = set(h.get('icf_codes', []))
        pred = set(get_pred_fn(h))
        
        tp = len(gt & pred)
        fp = len(pred - gt)
        fn = len(gt - pred)
        
        total_tp += tp
        total_fp += fp
        total_fn += fn
        
        if gt == pred:
            exact_matches += 1
            
    p = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    r = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    emr_pct = (exact_matches / n) * 100.0
    
    return {'f1': f1, 'emr_pct': emr_pct, 'exact_n': exact_matches, 'n': n, 'p': p, 'r': r}

estrategias = [
    ('Pase Único (K=1)', 'Iteración 1', lambda h: h.get('predicted_icf_it1', [])),
    ('Pase Único (K=1)', 'Iteración 2', lambda h: h.get('predicted_icf_it2', [])),
    ('Pase Único (K=1)', 'Iteración 3', lambda h: h.get('predicted_icf_it3', [])),
    ('Multi-Pase (K=3)', 'Consenso Estricto (3/3)', lambda h: set(h.get('predicted_icf_it1', [])) & set(h.get('predicted_icf_it2', [])) & set(h.get('predicted_icf_it3', []))),
    ('Multi-Pase (K=3)', 'Voto Mayoritario (≥ 2/3)', lambda h: [c for c in set(h.get('predicted_icf_it1', []) + h.get('predicted_icf_it2', []) + h.get('predicted_icf_it3', [])) if (c in h.get('predicted_icf_it1', [])) + (c in h.get('predicted_icf_it2', [])) + (c in h.get('predicted_icf_it3', [])) >= 2]),
    ('Multi-Pase (K=3)', 'Unión / Sensibilidad (≥ 1/3)', lambda h: set(h.get('predicted_icf_it1', []) + h.get('predicted_icf_it2', []) + h.get('predicted_icf_it3', [])))
]

datos_modelos = {}
for m in modelos:
    with open(m['archivo'], encoding='utf-8') as f:
        historias = json.load(f)
    res_m = {}
    for bloque, est_nom, fn in estrategias:
        res_m[est_nom] = evaluar_estrategia(historias, fn)
    datos_modelos[m['id']] = res_m

print('=== ESTRATEGIAS DE CONSENSO Y EFICIENCIA (DATOS REALES N=114) ===')
print(f"{'Estrategia':<30} | {'Gemma F1':<10} | {'Gemma EMR':<10} | {'Flash 3.5 F1':<12} | {'Flash 3.5 EMR':<12} | {'Flash 3.7 F1':<12} | {'Flash 3.7 EMR':<12}")
print('-' * 110)

salida_json = {}
for bloque, est_nom, _ in estrategias:
    g = datos_modelos['gemma_31b'][est_nom]
    f35 = datos_modelos['gemini_flash_35'][est_nom]
    f37 = datos_modelos['gemini_flash_37'][est_nom]
    print(f"{est_nom:<30} | {g['f1']:.4f}     | {g['emr_pct']:.2f}%     | {f35['f1']:.4f}       | {f35['emr_pct']:.2f}%       | {f37['f1']:.4f}       | {f37['emr_pct']:.2f}%")
    salida_json[est_nom] = {
        'bloque': bloque,
        'gemma': g,
        'flash_35': f35,
        'flash_37': f37
    }

out_path = llm_dir / 'resumen_estrategias_consenso.json'
out_path.write_text(json.dumps(salida_json, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'\nGuardado JSON dinámico en: {out_path}')
