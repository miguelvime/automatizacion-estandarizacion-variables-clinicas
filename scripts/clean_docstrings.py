# -*- coding: utf-8 -*-
from pathlib import Path

SCRIPTS_DIR = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis')

for name in ['04_calculo_sensibilidad_ablacion.py', '13_analisis_human_annotated.py', '14_plot_human_annotated.py']:
    p = SCRIPTS_DIR / name
    t = p.read_text(encoding='utf-8')
    t = t.replace('FLASH 3.6', 'FLASH 3.7')
    t = t.replace('Flash 3.6', 'Flash 3.7')
    p.write_text(t, encoding='utf-8')

print('Cleaned docstrings')
