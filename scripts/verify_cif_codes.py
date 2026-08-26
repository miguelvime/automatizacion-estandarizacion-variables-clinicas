# -*- coding: utf-8 -*-
import json
from pathlib import Path

base_dir = Path('/home/miguelvime/projects/2026-03-11_TFM')
llm_dir = base_dir / 'results' / 'llm_text'
human_dir = base_dir / 'results' / 'human_text'

OFFICIAL_24_CIF = {
    # Funciones Corporales (b) - 9 codigos
    'b130': 'Funciones de la energia y los impulsos',
    'b134': 'Funciones del sueno',
    'b147': 'Funciones psicomotoras',
    'b152': 'Funciones emocionales',
    'b1602': 'Contenido del pensamiento',
    'b280': 'Sensacion de dolor',
    'b455': 'Tolerancia al ejercicio fisico',
    'b730': 'Funciones relacionadas con la fuerza muscular',
    'b760': 'Control de los movimientos voluntarios',
    # Actividades y Participacion (d) - 10 codigos
    'd175': 'Resolver problemas',
    'd230': 'Llevar a cabo rutinas diarias',
    'd240': 'Manejo del estres y demandas psicologicas',
    'd430': 'Levantar y llevar objetos',
    'd450': 'Andar y desplazarse',
    'd640': 'Realizar los quehaceres de la casa',
    'd760': 'Relaciones familiares',
    'd770': 'Relaciones intimas y sociales',
    'd850': 'Trabajo remunerado',
    'd920': 'Tiempo libre y ocio',
    # Factores Ambientales (e) - 5 codigos
    'e1101': 'Medicamentos',
    'e310': 'Familiares cercanos',
    'e355': 'Profesionales de la salud',
    'e410': 'Actitudes individuales de miembros de la familia cercana',
    'e570': 'Servicios, sistemas y politicas de seguridad social'
}

print(f'Total Official Core Set Categories: {len(OFFICIAL_24_CIF)}')

def check_file(path, label):
    data = json.loads(path.read_text(encoding='utf-8'))
    all_gt = set()
    all_pred = set()
    for item in data:
        all_gt.update(item.get('icf_codes', []))
        all_pred.update(item.get('predicted_icf_codes_consensus', []))
        all_pred.update(item.get('predicted_icf_it1', []))
        all_pred.update(item.get('predicted_icf_it2', []))
        all_pred.update(item.get('predicted_icf_it3', []))
    
    gt_diff = all_gt - set(OFFICIAL_24_CIF.keys())
    pred_diff = all_pred - set(OFFICIAL_24_CIF.keys())
    print(f'[{label}] {path.name}: GT codes count={len(all_gt)}, Pred codes count={len(all_pred)}')
    if gt_diff:
        print(f'   ⚠️ Unexpected GT codes: {gt_diff}')
    if pred_diff:
        print(f'   ⚠️ Unexpected Pred codes (hallucinated outside 24): {pred_diff}')

for p in sorted(llm_dir.glob('*.json')):
    check_file(p, 'LLM')

for p in sorted(human_dir.glob('*.json')):
    check_file(p, 'HUMAN')
