# -*- coding: utf-8 -*-
from pathlib import Path

p = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis/09_generar_tablas_apa.R')
t = p.read_text(encoding='utf-8')
t = t.replace('Espacio ontológico (114 × 27)', 'Espacio ontológico (114 × 24)')
t = t.replace('"3.078"', '"2.736"')
t = t.replace('27 categorías', '24 categorías')
t = t.replace('27 Categorías', '24 Categorías')
p.write_text(t, encoding='utf-8')
print('Updated 09_generar_tablas_apa.R')
