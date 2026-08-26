# -*- coding: utf-8 -*-
from pathlib import Path

scripts_dir = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis')

# 1. 06_plot_desempeno.py
p6 = scripts_dir / '06_plot_desempeno.py'
t6 = p6.read_text(encoding='utf-8')
# Remove ax.axhline(0.80, color="#E74C3C", linestyle="--", linewidth=1.0, alpha=0.7, label="Umbral de Excelencia (≥ 0.80)")
t6 = t6.replace('    ax.axhline(0.80, color="#E74C3C", linestyle="--", linewidth=1.0, alpha=0.7, label="Umbral de Excelencia (≥ 0.80)")\n', '')
# Remove ax.axvline(0.80, color="#E74C3C", linestyle="--", linewidth=1.0, alpha=0.7, label="Umbral Aceptable (≥ 0.80)")
t6 = t6.replace('    ax.axvline(0.80, color="#E74C3C", linestyle="--", linewidth=1.0, alpha=0.7, label="Umbral Aceptable (≥ 0.80)")\n', '')
p6.write_text(t6, encoding='utf-8')
print('[OK] Threshold lines removed from 06_plot_desempeno.py')

# 2. 14_plot_human_annotated.py
p14 = scripts_dir / '14_plot_human_annotated.py'
t14 = p14.read_text(encoding='utf-8')
# Remove ax.axvline(0.80, color='#C0392B', linestyle='--', alpha=0.75, linewidth=1.2, label='Umbral Excelencia (0.80)')
t14 = t14.replace("    ax.axvline(0.80, color='#C0392B', linestyle='--', alpha=0.75, linewidth=1.2, label='Umbral Excelencia (0.80)')\n", '')
p14.write_text(t14, encoding='utf-8')
print('[OK] Threshold lines removed from 14_plot_human_annotated.py')
