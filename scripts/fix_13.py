# -*- coding: utf-8 -*-
from pathlib import Path

p = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis/13_analisis_human_annotated.py')
t = p.read_text(encoding='utf-8')
t = t.replace(
    "'flash_36': {'fiabilidad': fiab36, 'desempeno': des36, 'ci_95': ci36},",
    "'flash_37': {'fiabilidad': fiab36, 'desempeno': des36, 'ci_95': ci36},\n        'flash_36': {'fiabilidad': fiab36, 'desempeno': des36, 'ci_95': ci36},"
)
p.write_text(t, encoding='utf-8')
print('Updated 13_analisis_human_annotated.py')
