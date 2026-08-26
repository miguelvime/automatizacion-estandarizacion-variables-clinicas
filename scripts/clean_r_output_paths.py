# -*- coding: utf-8 -*-
from pathlib import Path

scripts_dir = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis')

# 1. 11_generar_tabla_consenso_apa.R -> write only tabla_apartado_5_3_eficiencia_apa.docx
p11 = scripts_dir / '11_generar_tabla_consenso_apa.R'
t11 = p11.read_text(encoding='utf-8')
t11 = t11.replace('ruta_docx_consenso    <- file.path(tablas_dir, "tabla_estrategias_consenso_apa.docx")\n', '')
t11 = t11.replace('ruta_docx_eficiencia  <- file.path(tablas_dir, "tabla_eficiencia_computacional.docx")\n', '')
t11 = t11.replace('print(doc, target = ruta_docx_consenso)\n', '')
t11 = t11.replace('print(doc, target = ruta_docx_eficiencia)\n', '')
t11 = t11.replace('cat("      -", ruta_docx_consenso, "\\n")\n', '')
t11 = t11.replace('cat("      -", ruta_docx_eficiencia, "\\n")\n', '')
p11.write_text(t11, encoding='utf-8')

# 2. 19_generar_tabla_caracteristicas_dataset_apa.R -> write only tabla_caracteristicas_dataset_apa.docx
p19 = scripts_dir / '19_generar_tabla_caracteristicas_dataset_apa.R'
t19 = p19.read_text(encoding='utf-8')
t19 = t19.replace('ruta_docx_53 <- file.path(tablas_dir, "tabla_apartado_5_3_caracteristicas_dataset_apa.docx")\n', '')
t19 = t19.replace('print(doc, target = ruta_docx_53)\n', '')
t19 = t19.replace('cat("      -", ruta_docx_53, "\\n")\n', '')
p19.write_text(t19, encoding='utf-8')

# 3. 09_generar_tablas_apa.R -> write tabla_desempeno_apa.docx and tablas_desempeno.docx
p9 = scripts_dir / '09_generar_tablas_apa.R'
t9 = p9.read_text(encoding='utf-8')
t9 = t9.replace('ruta_salida_docx <- file.path(tablas_dir, "tablas_desempeno.docx")', 'ruta_salida_docx <- file.path(tablas_dir, "tabla_desempeno_apa.docx")')
p9.write_text(t9, encoding='utf-8')

print('Cleaned R script outputs.')
