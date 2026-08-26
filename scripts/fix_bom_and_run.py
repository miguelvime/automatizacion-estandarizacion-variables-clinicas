# -*- coding: utf-8 -*-
from pathlib import Path

scripts_dir = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis')

# 1. Update 13
p13 = scripts_dir / '13_analisis_human_annotated.py'
t13 = p13.read_text(encoding='utf-8-sig')
if "'flash_37'" not in t13:
    t13 = t13.replace(
        "'flash_36': {'fiabilidad': fiab36, 'desempeno': des36, 'ci_95': ci36},",
        "'flash_37': {'fiabilidad': fiab36, 'desempeno': des36, 'ci_95': ci36},\n        'flash_36': {'fiabilidad': fiab36, 'desempeno': des36, 'ci_95': ci36},"
    )
p13.write_bytes(t13.encode('utf-8'))

# 2. Strip BOM from all scripts in scripts/analysis
for p in scripts_dir.glob('*.*'):
    raw = p.read_bytes()
    if raw.startswith(b'\xef\xbb\xbf'):
        p.write_bytes(raw[3:])
        print(f'Stripped BOM from {p.name}')

print('All scripts cleaned and ready.')
