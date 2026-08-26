# -*- coding: utf-8 -*-
from pathlib import Path

scripts_dir = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis')

# 1. 06_plot_desempeno.py
p6 = scripts_dir / '06_plot_desempeno.py'
t6 = p6.read_text(encoding='utf-8')
t6 = t6.replace('f"{val:.3f}" if val < 1.0 else f"{val:.1f}"', 'f"{val:.2f}" if val < 1.0 else f"{val:.1f}"')
t6 = t6.replace('f"{val:.3f}"', 'f"{val:.2f}"')
p6.write_text(t6, encoding='utf-8')
print('[OK] 06_plot_desempeno.py updated to 2 decimals')

# 2. 07_plot_eficiencia_f1.py
p7 = scripts_dir / '07_plot_eficiencia_f1.py'
t7 = p7.read_text(encoding='utf-8')
t7 = t7.replace('f"{y_pos:.4f}"', 'f"{y_pos:.2f}"')
p7.write_text(t7, encoding='utf-8')
print('[OK] 07_plot_eficiencia_f1.py updated to 2 decimals')

# 3. 14_plot_human_annotated.py
p14 = scripts_dir / '14_plot_human_annotated.py'
t14 = p14.read_text(encoding='utf-8')
t14 = t14.replace("f'{val:.3f}'", "f'{val:.2f}'")
t14 = t14.replace("f'{bar.get_height():.3f}'", "f'{bar.get_height():.2f}'")
p14.write_text(t14, encoding='utf-8')
print('[OK] 14_plot_human_annotated.py updated to 2 decimals')

# 4. 05_generar_tfl_fiabilidad.py
p5 = scripts_dir / '05_generar_tfl_fiabilidad.py'
t5 = p5.read_text(encoding='utf-8')
t5 = t5.replace('f"{height/100:.4f}"', 'f"{height/100:.2f}"')
p5.write_text(t5, encoding='utf-8')
print('[OK] 05_generar_tfl_fiabilidad.py updated to 2 decimals')
