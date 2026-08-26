# -*- coding: utf-8 -*-
from pathlib import Path

scripts_dir = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis')

# 1. Update 03_calculo_f1_score.py
p03 = scripts_dir / '03_calculo_f1_score.py'
t03 = p03.read_text(encoding='utf-8')
t03 = t03.replace('2026-08-11_gemma-4-31b-it-codified.json', '2026-08-25_gemma_codified.json')
t03 = t03.replace('2026-08-18_gemini-flash-3.5_codified.json', '2026-08-25-flash-3.5-codified.json')
t03 = t03.replace('2026-08-18_gemini-flash-3.6_codified.json', '2026-08-25-3.7-flash-codified.json')
t03 = t03.replace('Espacio de decisiones ontológicas (114 × 27)', 'Espacio de decisiones ontológicas (114 × 24)')
t03 = t03.replace('"3.078"', '"2.736"')
t03 = t03.replace('27 categorías', '24 categorías')
t03 = t03.replace('27 Categorías', '24 Categorías')
p03.write_text(t03, encoding='utf-8')
print('03_calculo_f1_score.py updated')

# 2. Update 04_calculo_sensibilidad_ablacion.py
p04 = scripts_dir / '04_calculo_sensibilidad_ablacion.py'
t04 = p04.read_text(encoding='utf-8')
t04 = t04.replace('2026-08-11_gemma-4-31b-it-codified.json', '2026-08-25_gemma_codified.json')
t04 = t04.replace('2026-08-18_gemini-flash-3.5_codified.json', '2026-08-25-flash-3.5-codified.json')
t04 = t04.replace('2026-08-18_gemini-flash-3.6_codified.json', '2026-08-25-3.7-flash-codified.json')
t04 = t04.replace('"27 códigos"', '"24 códigos"')
t04 = t04.replace('27 categorías', '24 categorías')
t04 = t04.replace('26 categorías', '23 categorías')
p04.write_text(t04, encoding='utf-8')
print('04_calculo_sensibilidad_ablacion.py updated')

# 3. Update 05_generar_tfl_fiabilidad.py
p05 = scripts_dir / '05_generar_tfl_fiabilidad.py'
t05 = p05.read_text(encoding='utf-8')
t05 = t05.replace('2026-08-11_gemma-4-31b-it-codified.json', '2026-08-25_gemma_codified.json')
t05 = t05.replace('2026-08-18_gemini-flash-3.5_codified.json', '2026-08-25-flash-3.5-codified.json')
t05 = t05.replace('2026-08-18_gemini-flash-3.6_codified.json', '2026-08-25-3.7-flash-codified.json')
t05 = t05.replace('27 códigos', '24 códigos')
t05 = t05.replace('3.078', '2.736')
p05.write_text(t05, encoding='utf-8')
print('05_generar_tfl_fiabilidad.py updated')

# 4. Update 13_analisis_human_annotated.py
p13 = scripts_dir / '13_analisis_human_annotated.py'
t13 = p13.read_text(encoding='utf-8')
t13 = t13.replace('human_annotated_flash-3.5.json', '2026-08-25-flash-3.5-human-annotated.json')
t13 = t13.replace('human_annotated_flash-3.6.json', '2026-08-25-flash-3.7-human-annotated.json')
t13 = t13.replace('human_annotated_gemma.json', '2026-08-26-gemma_human_annotated.json')
p13.write_text(t13, encoding='utf-8')
print('13_analisis_human_annotated.py updated')
