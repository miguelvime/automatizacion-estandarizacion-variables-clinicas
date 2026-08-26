# -*- coding: utf-8 -*-
"""
Script de refactorización y auditoría: Actualiza todas las referencias de modelos
a los nombres y rutas oficiales vigentes:
- Gemma-4-31B-it (Local)
- Gemini Flash 3.5 (Cloud)
- Gemini Flash 3.7 (Cloud)
"""

from pathlib import Path
import re

SCRIPTS_DIR = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis')

# 1. 01_calculo_confiabilidad_azar.py
p = SCRIPTS_DIR / '01_calculo_confiabilidad_azar.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('gemini_flash_36', 'gemini_flash_37')
p.write_text(t, encoding='utf-8')
print('[OK] 01_calculo_confiabilidad_azar.py')

# 2. 02_calculo_acuerdo_exacto.py
p = SCRIPTS_DIR / '02_calculo_acuerdo_exacto.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('gemini_flash_36', 'gemini_flash_37')
p.write_text(t, encoding='utf-8')
print('[OK] 02_calculo_acuerdo_exacto.py')

# 3. 03_calculo_f1_score.py
p = SCRIPTS_DIR / '03_calculo_f1_score.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('gemini_flash_36', 'gemini_flash_37')
t = t.replace('Flash 3.6', 'Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 03_calculo_f1_score.py')

# 4. 04_calculo_sensibilidad_ablacion.py
p = SCRIPTS_DIR / '04_calculo_sensibilidad_ablacion.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('gemini_flash_36', 'gemini_flash_37')
t = t.replace('Flash 3.6', 'Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 04_calculo_sensibilidad_ablacion.py')

# 5. 05_generar_tfl_fiabilidad.py
p = SCRIPTS_DIR / '05_generar_tfl_fiabilidad.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('gemini_flash_36', 'gemini_flash_37')
t = t.replace('Flash 3.6', 'Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 05_generar_tfl_fiabilidad.py')

# 6. 06_plot_desempeno.py
p = SCRIPTS_DIR / '06_plot_desempeno.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('gemini_flash_36', 'gemini_flash_37')
t = t.replace('Flash 3.6', 'Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 06_plot_desempeno.py')

# 7. 07_plot_eficiencia_f1.py
p = SCRIPTS_DIR / '07_plot_eficiencia_f1.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('gemini_flash_36', 'gemini_flash_37')
t = t.replace('Flash 3.6', 'Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 07_plot_eficiencia_f1.py')

# 8. 08_plot_sensibilidad_ablacion.py
p = SCRIPTS_DIR / '08_plot_sensibilidad_ablacion.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('gemini_flash_36', 'gemini_flash_37')
t = t.replace('Flash 3.6', 'Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 08_plot_sensibilidad_ablacion.py')

# 9. 09_generar_tablas_apa.R
p = SCRIPTS_DIR / '09_generar_tablas_apa.R'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('Flash 3.6', 'Flash 3.7')
t = t.replace('Flash_36', 'Flash_37')
p.write_text(t, encoding='utf-8')
print('[OK] 09_generar_tablas_apa.R')

# 10. 10_generar_tabla_fiabilidad_apa.R
p = SCRIPTS_DIR / '10_generar_tabla_fiabilidad_apa.R'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('Flash 3.6', 'Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 10_generar_tabla_fiabilidad_apa.R')

# 11. 11_generar_tabla_consenso_apa.R
p = SCRIPTS_DIR / '11_generar_tabla_consenso_apa.R'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('Flash 3.6', 'Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 11_generar_tabla_consenso_apa.R')

# 12. 12_tabla_sensibilidad_ablacion_apa.R
p = SCRIPTS_DIR / '12_tabla_sensibilidad_ablacion_apa.R'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('Flash 3.6', 'Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 12_tabla_sensibilidad_ablacion_apa.R')

# 13. 13_analisis_human_annotated.py
p = SCRIPTS_DIR / '13_analisis_human_annotated.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('F36_PATH', 'F37_PATH')
t = t.replace('f36', 'f37')
t = t.replace('Flash 3.6', 'Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 13_analisis_human_annotated.py')

# 14. 14_plot_human_annotated.py
p = SCRIPTS_DIR / '14_plot_human_annotated.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('flash_36', 'flash_37')
t = t.replace('Flash 3.6', 'Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 14_plot_human_annotated.py')

# 15. 15_generar_tablas_human_apa.R
p = SCRIPTS_DIR / '15_generar_tablas_human_apa.R'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('flash_36', 'flash_37')
t = t.replace('Flash 3.6', 'Flash 3.7')
t = t.replace('f36', 'f37')
p.write_text(t, encoding='utf-8')
print('[OK] 15_generar_tablas_human_apa.R')

# 16. 16_generar_informe_word_completo.py
p = SCRIPTS_DIR / '16_generar_informe_word_completo.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('flash_36', 'flash_37')
t = t.replace('Flash 3.6', 'Flash 3.7')
t = t.replace('f36', 'f37')
t = t.replace('s36', 's37')
p.write_text(t, encoding='utf-8')
print('[OK] 16_generar_informe_word_completo.py')

# 17. 17_workflow_diagram.py
p = SCRIPTS_DIR / '17_workflow_diagram.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini-3.6-flash', 'Gemini-3.7-flash')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
p.write_text(t, encoding='utf-8')
print('[OK] 17_workflow_diagram.py')

# 18. 18_generar_dashboard_html.py
p = SCRIPTS_DIR / '18_generar_dashboard_html.py'
t = p.read_text(encoding='utf-8')
t = t.replace('human_annotated_flash-3.6.json', '2026-08-25-flash-3.7-human-annotated.json')
t = t.replace('human_annotated_flash-3.5.json', '2026-08-25-flash-3.5-human-annotated.json')
t = t.replace('human_annotated_gemma.json', '2026-08-26-gemma_human_annotated.json')
t = t.replace('Google Gemini Flash 3.6', 'Google Gemini Flash 3.7')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('flash_36', 'flash_37')
t = t.replace('flash36', 'flash37')
p.write_text(t, encoding='utf-8')
print('[OK] 18_generar_dashboard_html.py')

# 19. ejecutar_todo.py
p = SCRIPTS_DIR / 'ejecutar_todo.py'
t = p.read_text(encoding='utf-8')
t = t.replace('Gemini Flash 3.6', 'Gemini Flash 3.7')
t = t.replace('flash_36', 'flash_37')
p.write_text(t, encoding='utf-8')
print('[OK] ejecutar_todo.py')
