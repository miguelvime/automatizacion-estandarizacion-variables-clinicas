# -*- coding: utf-8 -*-
from pathlib import Path

scripts_dir = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis')

for p in scripts_dir.glob('*.*'):
    if p.suffix in ['.py', '.R']:
        t = p.read_text(encoding='utf-8')
        t = t.replace('Gemma-4-31B-it (Local)', 'Gemma-4-31B-it')
        t = t.replace('Gemini Flash 3.5 (Cloud)', 'Gemini Flash 3.5')
        t = t.replace('Gemini Flash 3.7 (Cloud)', 'Gemini Flash 3.7')
        t = t.replace('Gemma-4-31B (Local)', 'Gemma-4-31B-it')
        t = t.replace('Gemma (Local)', 'Gemma-4-31B-it')
        t = t.replace('Flash 3.5 (Cloud)', 'Gemini Flash 3.5')
        t = t.replace('Flash 3.7 (Cloud)', 'Gemini Flash 3.7')
        t = t.replace(' (Local)', '')
        t = t.replace(' (Cloud)', '')
        t = t.replace(' (local)', '')
        t = t.replace(' (cloud)', '')
        p.write_text(t, encoding='utf-8')
        print(f'[OK] Cleaned {p.name}')

print('All scripts cleaned of (Local) and (Cloud) labels.')
