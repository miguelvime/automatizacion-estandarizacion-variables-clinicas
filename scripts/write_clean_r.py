# -*- coding: utf-8 -*-
from pathlib import Path

scripts_dir = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis')

# 10_generar_tabla_fiabilidad_apa.R
(scripts_dir / '10_generar_tabla_fiabilidad_apa.R').write_text('''# -*- coding: utf-8 -*-
suppressPackageStartupMessages({
  library(dplyr)
  library(flextable)
  library(officer)
  library(magrittr)
  library(jsonlite)
})

base_dir <- tryCatch({
  this_file <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("--file=", this_file, value = TRUE)
  if (length(file_arg) > 0) {
    dirname(dirname(dirname(normalizePath(sub("--file=", "", file_arg)))))
  } else {
    "/home/miguelvime/projects/2026-03-11_TFM"
  }
}, error = function(e) {
  "/home/miguelvime/projects/2026-03-11_TFM"
})

tablas_dir  <- file.path(base_dir, "results", "TFL", "tablas")
llm_dir     <- file.path(base_dir, "results", "llm_text")
ruta_salida_docx <- file.path(tablas_dir, "tabla_fiabilidad_apa.docx")
json_path <- file.path(llm_dir, "resumen_fiabilidad.json")

border_main <- fp_border(color = "#222222", width = 1.5)
border_sub  <- fp_border(color = "#444444", width = 0.8)

fiab_data <- fromJSON(json_path)
gemma <- fiab_data$gemma_31b
f35   <- fiab_data$gemini_flash_35
f37   <- fiab_data$gemini_flash_37

df_transpuesta <- tibble::tribble(
  ~Dimension, ~Metrica, ~Gemma_31B, ~Flash_35, ~Flash_37,
  "Corpus Clínico", "Historias Clínicas Evaluadas (N)", "114", "114", "114",
  "Corpus Clínico", "Iteraciones Independientes (K)", "3", "3", "3",
  "Corpus Clínico", "Espacio de Decisiones Binarias (114 × 24)", "2.736", "2.736", "2.736",
  
  "Acuerdo Multietiqueta", "Acuerdo Exacto Consensuado 3/3 (n / N)", sprintf("%d / %d", as.integer(gemma$emr_acuerdos), as.integer(gemma$historias)), sprintf("%d / %d", as.integer(f35$emr_acuerdos), as.integer(f35$historias)), sprintf("%d / %d", as.integer(f37$emr_acuerdos), as.integer(f37$historias)),
  "Acuerdo Multietiqueta", "Exact Match Ratio (EMR %)", sprintf("%.2f%%", as.numeric(gemma$emr_pct)), sprintf("%.2f%%", as.numeric(f35$emr_pct)), sprintf("%.2f%%", as.numeric(f37$emr_pct)),
  
  "Confiabilidad Ajustada", "Acuerdo Observado Po (%)", sprintf("%.4f%%", as.numeric(gemma$Po) * 100), sprintf("%.4f%%", as.numeric(f35$Po) * 100), sprintf("%.4f%%", as.numeric(f37$Po) * 100),
  "Confiabilidad Ajustada", "Coeficiente Gwet's AC1", sprintf("%.4f", as.numeric(gemma$Gwet_AC1)), sprintf("%.4f", as.numeric(f35$Gwet_AC1)), sprintf("%.4f", as.numeric(f37$Gwet_AC1)),
  "Confiabilidad Ajustada", "Alpha de Krippendorff (α)", sprintf("%.4f", as.numeric(gemma$Krippendorff_Alpha)), sprintf("%.4f", as.numeric(f35$Krippendorff_Alpha)), sprintf("%.4f", as.numeric(f37$Krippendorff_Alpha))
)

ft_transpuesta <- flextable(df_transpuesta) %>%
  set_header_labels(
    Dimension = "Dimensión",
    Metrica = "Métrica de Reproducibilidad",
    Gemma_31B = "Gemma-4-31B-it (Local)",
    Flash_35 = "Gemini Flash 3.5 (Cloud)",
    Flash_37 = "Gemini Flash 3.7 (Cloud)"
  ) %>%
  merge_v(j = "Dimension") %>%
  valign(j = "Dimension", valign = "top") %>%
  italic(j = "Dimension") %>%
  bold(part = "header") %>%
  bold(i = c(5, 7, 8), j = c("Metrica", "Gemma_31B", "Flash_35", "Flash_37")) %>%
  align(j = 1:2, align = "left", part = "all") %>%
  align(j = 3:5, align = "center", part = "all") %>%
  border_remove() %>%
  hline_top(part = "header", border = border_main) %>%
  hline_bottom(part = "header", border = border_sub) %>%
  hline_bottom(part = "body", border = border_main) %>%
  hline(i = c(3, 5), border = border_sub) %>%
  padding(padding.top = 4, padding.bottom = 4, padding.left = 6, padding.right = 6, part = "all") %>%
  fontsize(size = 9.5, part = "all") %>%
  fontsize(size = 10, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  width(j = 1, width = 1.4) %>%
  width(j = 2, width = 2.4) %>%
  width(j = 3:5, width = 1.25) %>%
  set_caption(caption = "Tabla 1. Confiabilidad y reproducibilidad inter-iteraciones en la codificación CIF.")

df_modelos_filas <- tibble::tribble(
  ~Modelo, ~Historias, ~Acuerdo_Exacto, ~EMR_pct, ~Po_pct, ~Gwets_AC1, ~Krippendorff_alpha,
  "Gemma-4-31B-it (Local)", as.character(gemma$historias), sprintf("%d / %d", as.integer(gemma$emr_acuerdos), as.integer(gemma$historias)), sprintf("%.2f%%", as.numeric(gemma$emr_pct)), sprintf("%.4f%%", as.numeric(gemma$Po) * 100), sprintf("%.4f", as.numeric(gemma$Gwet_AC1)), sprintf("%.4f", as.numeric(gemma$Krippendorff_Alpha)),
  "Gemini Flash 3.5 (Cloud)", as.character(f35$historias), sprintf("%d / %d", as.integer(f35$emr_acuerdos), as.integer(f35$historias)), sprintf("%.2f%%", as.numeric(f35$emr_pct)), sprintf("%.4f%%", as.numeric(f35$Po) * 100), sprintf("%.4f", as.numeric(f35$Gwet_AC1)), sprintf("%.4f", as.numeric(f35$Krippendorff_Alpha)),
  "Gemini Flash 3.7 (Cloud)", as.character(f37$historias), sprintf("%d / %d", as.integer(f37$emr_acuerdos), as.integer(f37$historias)), sprintf("%.2f%%", as.numeric(f37$emr_pct)), sprintf("%.4f%%", as.numeric(f37$Po) * 100), sprintf("%.4f", as.numeric(f37$Gwet_AC1)), sprintf("%.4f", as.numeric(f37$Krippendorff_Alpha))
)

ft_filas <- flextable(df_modelos_filas) %>%
  set_header_labels(
    Modelo = "Modelo LLM",
    Historias = "Historias (N)",
    Acuerdo_Exacto = "Acuerdo 3/3 (n)",
    EMR_pct = "Exact Match (%)",
    Po_pct = "Acuerdo Po (%)",
    Gwets_AC1 = "Gwet's AC1",
    Krippendorff_alpha = "Krippendorff α"
  ) %>%
  bold(j = "Modelo") %>%
  bold(part = "header") %>%
  align(j = 1, align = "left", part = "all") %>%
  align(j = 2:7, align = "center", part = "all") %>%
  border_remove() %>%
  hline_top(part = "header", border = border_main) %>%
  hline_bottom(part = "header", border = border_sub) %>%
  hline_bottom(part = "body", border = border_main) %>%
  padding(padding.top = 4, padding.bottom = 4, padding.left = 6, padding.right = 6, part = "all") %>%
  fontsize(size = 9.5, part = "all") %>%
  fontsize(size = 10, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  width(j = 1, width = 1.8) %>%
  width(j = 2:7, width = 0.90) %>%
  set_caption(caption = "Tabla 2. Métricas de consistencia y confiabilidad inter-iteraciones por modelo LLM.")

doc <- read_docx() %>%
  body_add_par("Confiabilidad y Reproducibilidad Inter-Iteraciones de los Modelos LLM", style = "heading 1") %>%
  body_add_par("Evaluación del acuerdo intra-modelo a través de 3 iteraciones independientes bajo temperatura controlada (114 historias clínicas, espacio de 2.736 decisiones ontológicas).", style = "Normal") %>%
  body_add_par("", style = "Normal") %>%
  body_add_par("Formato Transpuesto (Modelos en Columnas)", style = "heading 2") %>%
  body_add_flextable(ft_transpuesta) %>%
  body_add_par("", style = "Normal") %>%
  body_add_par("", style = "Normal") %>%
  body_add_par("Formato Clásico (Modelos en Filas)", style = "heading 2") %>%
  body_add_flextable(ft_filas)

print(doc, target = ruta_salida_docx)
cat(" [OK] Documento exportado a:", ruta_salida_docx, "\n")
''', encoding='utf-8')

# 11_generar_tabla_consenso_apa.R
(scripts_dir / '11_generar_tabla_consenso_apa.R').write_text('''# -*- coding: utf-8 -*-
suppressPackageStartupMessages({
  library(dplyr)
  library(flextable)
  library(officer)
  library(magrittr)
  library(jsonlite)
})

base_dir <- tryCatch({
  this_file <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("--file=", this_file, value = TRUE)
  if (length(file_arg) > 0) {
    dirname(dirname(dirname(normalizePath(sub("--file=", "", file_arg)))))
  } else {
    "/home/miguelvime/projects/2026-03-11_TFM"
  }
}, error = function(e) {
  "/home/miguelvime/projects/2026-03-11_TFM"
})

tablas_dir  <- file.path(base_dir, "results", "TFL", "tablas")
llm_dir     <- file.path(base_dir, "results", "llm_text")
dir.create(tablas_dir, showWarnings = FALSE, recursive = TRUE)

ruta_docx_consenso    <- file.path(tablas_dir, "tabla_estrategias_consenso_apa.docx")
ruta_docx_eficiencia  <- file.path(tablas_dir, "tabla_eficiencia_computacional.docx")
ruta_docx_apartado_53 <- file.path(tablas_dir, "tabla_apartado_5_3_eficiencia_apa.docx")
json_path             <- file.path(llm_dir, "resumen_estrategias_consenso.json")

border_main <- fp_border(color = "#222222", width = 1.5)
border_sub  <- fp_border(color = "#444444", width = 0.8)

cons_data <- fromJSON(json_path)

est_names <- c(
  "Iteración 1", "Iteración 2", "Iteración 3",
  "Consenso Estricto (3/3)", "Voto Mayoritario (≥ 2/3)", "Unión / Sensibilidad (≥ 1/3)"
)

costes <- c("1x (Óptimo)", "1x", "1x", "3x", "3x", "3x")

filas <- list()
for (i in seq_along(est_names)) {
  nom <- est_names[i]
  item <- cons_data[[nom]]
  filas[[length(filas) + 1]] <- list(
    Estrategia_inferencia = as.character(item$bloque),
    Estrategia_Decision   = nom,
    Coste_Relativo        = costes[i],
    Gemma_F1              = sprintf("%.4f", as.numeric(item$gemma$f1)),
    Gemma_EMR             = sprintf("%.2f%%", as.numeric(item$gemma$emr_pct)),
    Flash35_F1            = sprintf("%.4f", as.numeric(item$flash_35$f1)),
    Flash35_EMR           = sprintf("%.2f%%", as.numeric(item$flash_35$emr_pct)),
    Flash37_F1            = sprintf("%.4f", as.numeric(item$flash_37$f1)),
    Flash37_EMR           = sprintf("%.2f%%", as.numeric(item$flash_37$emr_pct))
  )
}

df_estrategias <- bind_rows(filas)

ft <- flextable(df_estrategias) %>%
  set_header_labels(
    Estrategia_inferencia = "Estrategia inferencia",
    Estrategia_Decision   = "Estrategia de Decisión",
    Coste_Relativo        = "Coste Relativo",
    Gemma_F1              = "Gemma (F1)",
    Gemma_EMR             = "Gemma (EMR)",
    Flash35_F1            = "Flash 3.5 (F1)",
    Flash35_EMR           = "Flash 3.5 (EMR)",
    Flash37_F1            = "Flash 3.7 (F1)",
    Flash37_EMR           = "Flash 3.7 (EMR)"
  ) %>%
  merge_v(j = "Estrategia_inferencia") %>%
  valign(j = "Estrategia_inferencia", valign = "top") %>%
  italic(j = "Estrategia_inferencia") %>%
  bold(part = "header") %>%
  align(j = 1:2, align = "left", part = "all") %>%
  align(j = 3:9, align = "center", part = "all") %>%
  border_remove() %>%
  hline_top(part = "header", border = border_main) %>%
  hline_bottom(part = "header", border = border_sub) %>%
  hline_bottom(part = "body", border = border_main) %>%
  hline(i = 3, border = border_sub) %>%
  padding(padding.top = 4.5, padding.bottom = 4.5, padding.left = 5, padding.right = 5, part = "all") %>%
  fontsize(size = 9.0, part = "body") %>%
  fontsize(size = 9.5, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  width(j = 1, width = 1.25) %>%
  width(j = 2, width = 1.70) %>%
  width(j = 3, width = 0.85) %>%
  width(j = 4:9, width = 0.60)

doc <- read_docx() %>%
  body_add_par("Apartado 5.3: Eficiencia Computacional y Estrategias de Inferencia", style = "heading 1") %>%
  body_add_par("Tabla . Análisis de eficiencia computacional y rendimiento diagnóstico según la estrategia de inferencia (Pase Único vs Consenso Multi-Pase).", style = "Normal") %>%
  body_add_flextable(ft) %>%
  body_add_par("Nota. K: Número de pasadas o ejecuciones independientes por caso clínico. F1: Puntuación Micro-F1 frente al Ground Truth (N = 114). EMR: Exact Match Ratio (% de concordancia exacta perfecta multietiqueta). 1x (Óptimo): Menor coste computacional y latencia por caso clínico.", style = "Normal")

print(doc, target = ruta_docx_apartado_53)
print(doc, target = ruta_docx_consenso)
print(doc, target = ruta_docx_eficiencia)

cat(" [OK] Tabla 5.3 generada con formato tfl-apa-tables en:\n")
cat("      -", ruta_docx_apartado_53, "\n")
cat("      -", ruta_docx_consenso, "\n")
cat("      -", ruta_docx_eficiencia, "\n")
''', encoding='utf-8')

# 15_generar_tablas_human_apa.R
(scripts_dir / '15_generar_tablas_human_apa.R').write_text('''# -*- coding: utf-8 -*-
suppressPackageStartupMessages({
  library(flextable)
  library(officer)
  library(magrittr)
  library(jsonlite)
  library(dplyr)
})

border_main  <- fp_border(color = "#222222", width = 1.5)
border_sub   <- fp_border(color = "#444444", width = 0.8)
border_light <- fp_border(color = "#D0D0D0", width = 0.5)

base_dir <- tryCatch({
  this_file <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("--file=", this_file, value = TRUE)
  if (length(file_arg) > 0) {
    dirname(dirname(dirname(normalizePath(sub("--file=", "", file_arg)))))
  } else {
    "/home/miguelvime/projects/2026-03-11_TFM"
  }
}, error = function(e) {
  "/home/miguelvime/projects/2026-03-11_TFM"
})

data_dir     <- file.path(base_dir, "data")
results_dir  <- file.path(base_dir, "results")
llm_dir      <- file.path(results_dir, "llm_text")
human_dir    <- file.path(results_dir, "human_text")
tfl_dir      <- file.path(results_dir, "TFL")
tablas_dir   <- file.path(tfl_dir, "tablas")
figuras_dir  <- file.path(tfl_dir, "figuras")
informes_dir <- file.path(tfl_dir, "informes")

json_path    <- file.path(human_dir, "resumen_human_annotated.json")
csv_path     <- file.path(human_dir, "tabla_per_class_human.csv")
synth_path   <- file.path(llm_dir, "resumen_f1_score.json")
fiab_path    <- file.path(llm_dir, "resumen_fiabilidad.json")
out_docx     <- file.path(tablas_dir, "tablas_validacion_humana_apa.docx")

res_hum      <- fromJSON(json_path)
res_syn      <- fromJSON(synth_path)
res_fiab     <- fromJSON(fiab_path)
df_per_class <- read.csv(csv_path, stringsAsFactors = FALSE, encoding = "UTF-8")

f35 <- res_hum$flash_35
f37 <- if (!is.null(res_hum$flash_37)) res_hum$flash_37 else res_hum$flash_36
fg  <- res_hum$gemma_31b

# ==============================================================================
# TABLA 1: DESEMPEÑO GLOBAL Y FIABILIDAD INTRA-MODELO (N=21)
# ==============================================================================
df_t1 <- data.frame(
  Dimension = c(
    rep("Corpus Clínico Humano", 5),
    rep("Fiabilidad Intra-Modelo", 4),
    rep("Matriz de Confusión", 4),
    rep("Nivel Micro (Global)", 3),
    rep("Nivel Macro (Promedio)", 3),
    rep("Nivel Weighted (Ponderado)", 3)
  ),
  Metrica = c(
    "Historias clínicas evaluadas (N)",
    "Espacio ontológico evaluado (N × 24)",
    "Soporte real de menciones CIF",
    "Promedio de códigos por historia",
    "Criterio de consenso multi-iteración",
    
    "Porcentaje de Acuerdo Exacto (PAE, %)",
    "Acuerdo Observado (Po, %)",
    "Coeficiente AC1 de Gwet",
    "Alfa (α) de Krippendorff",
    
    "Verdaderos Positivos (TP)",
    "Falsos Positivos / Alucinaciones (FP)",
    "Falsos Negativos / Omisiones (FN)",
    "Exact Match Ratio (EMR, %)",
    
    "Precisión Micro",
    "Sensibilidad / Recall Micro",
    "Micro-F1 [IC 95% Bootstrap]",
    
    "Precisión Macro",
    "Sensibilidad / Recall Macro",
    "Macro-F1 [IC 95% Bootstrap]",
    
    "Precisión Weighted",
    "Sensibilidad / Recall Weighted",
    "Weighted-F1 [IC 95% Bootstrap]"
  ),
  Gemma_31B = c(
    "21", "504", "115", "5.48 ± 2.56", "Consenso estricto (3/3)",
    sprintf("%.2f%%", as.numeric(fg$fiabilidad$pae_pct)),
    sprintf("%.2f%%", as.numeric(fg$fiabilidad$Po) * 100),
    sprintf("%.4f", as.numeric(fg$fiabilidad$ac1)),
    sprintf("%.4f", as.numeric(fg$fiabilidad$alpha)),
    as.character(fg$desempeno$tp),
    as.character(fg$desempeno$fp),
    as.character(fg$desempeno$fn),
    sprintf("%.2f%% (%d/21)", as.numeric(fg$desempeno$emr), as.integer(fg$desempeno$exact)),
    sprintf("%.4f", as.numeric(fg$desempeno$micro$p)),
    sprintf("%.4f", as.numeric(fg$desempeno$micro$r)),
    sprintf("%.4f [%.4f, %.4f]", as.numeric(fg$desempeno$micro$f1), as.numeric(fg$ci_95$micro[[1]]), as.numeric(fg$ci_95$micro[[2]])),
    sprintf("%.4f", as.numeric(fg$desempeno$macro$p)),
    sprintf("%.4f", as.numeric(fg$desempeno$macro$r)),
    sprintf("%.4f [%.4f, %.4f]", as.numeric(fg$desempeno$macro$f1), as.numeric(fg$ci_95$macro[[1]]), as.numeric(fg$ci_95$macro[[2]])),
    sprintf("%.4f", as.numeric(fg$desempeno$weighted$p)),
    sprintf("%.4f", as.numeric(fg$desempeno$weighted$r)),
    sprintf("%.4f [%.4f, %.4f]", as.numeric(fg$desempeno$weighted$f1), as.numeric(fg$ci_95$weighted[[1]]), as.numeric(fg$ci_95$weighted[[2]]))
  ),
  Flash_35 = c(
    "21", "504", "115", "5.48 ± 2.56", "Consenso estricto (3/3)",
    sprintf("%.2f%%", as.numeric(f35$fiabilidad$pae_pct)),
    sprintf("%.2f%%", as.numeric(f35$fiabilidad$Po) * 100),
    sprintf("%.4f", as.numeric(f35$fiabilidad$ac1)),
    sprintf("%.4f", as.numeric(f35$fiabilidad$alpha)),
    as.character(f35$desempeno$tp),
    as.character(f35$desempeno$fp),
    as.character(f35$desempeno$fn),
    sprintf("%.2f%% (%d/21)", as.numeric(f35$desempeno$emr), as.integer(f35$desempeno$exact)),
    sprintf("%.4f", as.numeric(f35$desempeno$micro$p)),
    sprintf("%.4f", as.numeric(f35$desempeno$micro$r)),
    sprintf("%.4f [%.4f, %.4f]", as.numeric(f35$desempeno$micro$f1), as.numeric(f35$ci_95$micro[[1]]), as.numeric(f35$ci_95$micro[[2]])),
    sprintf("%.4f", as.numeric(f35$desempeno$macro$p)),
    sprintf("%.4f", as.numeric(f35$desempeno$macro$r)),
    sprintf("%.4f [%.4f, %.4f]", as.numeric(f35$desempeno$macro$f1), as.numeric(f35$ci_95$macro[[1]]), as.numeric(f35$ci_95$macro[[2]])),
    sprintf("%.4f", as.numeric(f35$desempeno$weighted$p)),
    sprintf("%.4f", as.numeric(f35$desempeno$weighted$r)),
    sprintf("%.4f [%.4f, %.4f]", as.numeric(f35$desempeno$weighted$f1), as.numeric(f35$ci_95$weighted[[1]]), as.numeric(f35$ci_95$weighted[[2]]))
  ),
  Flash_37 = c(
    "21", "504", "115", "5.48 ± 2.56", "Consenso estricto (3/3)",
    sprintf("%.2f%%", as.numeric(f37$fiabilidad$pae_pct)),
    sprintf("%.2f%%", as.numeric(f37$fiabilidad$Po) * 100),
    sprintf("%.4f", as.numeric(f37$fiabilidad$ac1)),
    sprintf("%.4f", as.numeric(f37$fiabilidad$alpha)),
    as.character(f37$desempeno$tp),
    as.character(f37$desempeno$fp),
    as.character(f37$desempeno$fn),
    sprintf("%.2f%% (%d/21)", as.numeric(f37$desempeno$emr), as.integer(f37$desempeno$exact)),
    sprintf("%.4f", as.numeric(f37$desempeno$micro$p)),
    sprintf("%.4f", as.numeric(f37$desempeno$micro$r)),
    sprintf("%.4f [%.4f, %.4f]", as.numeric(f37$desempeno$micro$f1), as.numeric(f37$ci_95$micro[[1]]), as.numeric(f37$ci_95$micro[[2]])),
    sprintf("%.4f", as.numeric(f37$desempeno$macro$p)),
    sprintf("%.4f", as.numeric(f37$desempeno$macro$r)),
    sprintf("%.4f [%.4f, %.4f]", as.numeric(f37$desempeno$macro$f1), as.numeric(f37$ci_95$macro[[1]]), as.numeric(f37$ci_95$macro[[2]])),
    sprintf("%.4f", as.numeric(f37$desempeno$weighted$p)),
    sprintf("%.4f", as.numeric(f37$desempeno$weighted$r)),
    sprintf("%.4f [%.4f, %.4f]", as.numeric(f37$desempeno$weighted$f1), as.numeric(f37$ci_95$weighted[[1]]), as.numeric(f37$ci_95$weighted[[2]]))
  ),
  stringsAsFactors = FALSE
)

tabla1_apa <- flextable(df_t1) %>%
  set_header_labels(
    Dimension = "Dimensión",
    Metrica   = "Métrica / Parámetro",
    Gemma_31B = "Gemma-4-31B-it (Local)",
    Flash_35  = "Gemini Flash 3.5 (Cloud)",
    Flash_37  = "Gemini Flash 3.7 (Cloud)"
  ) %>%
  merge_v(j = "Dimension") %>%
  valign(j = "Dimension", valign = "top") %>%
  italic(j = "Dimension") %>%
  bold(part = "header") %>%
  align(j = 1:2, align = "left", part = "all") %>%
  align(j = 3:5, align = "center", part = "all") %>%
  border_remove() %>%
  hline_top(part = "header", border = border_main) %>%
  hline_bottom(part = "header", border = border_sub) %>%
  hline_bottom(part = "body", border = border_main) %>%
  hline(i = c(5, 9, 13, 16, 19), border = border_sub) %>%
  padding(padding.top = 3.5, padding.bottom = 3.5, padding.left = 5, padding.right = 5, part = "all") %>%
  fontsize(size = 9, part = "body") %>%
  fontsize(size = 9.5, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  autofit()

# ==============================================================================
# TABLA 2: AUDITORÍA PER-CLASS POR CATEGORÍA CIF
# ==============================================================================
df_t2 <- data.frame(
  Componente = df_per_class$componente_nombre,
  Codigo     = df_per_class$codigo,
  Categoria  = df_per_class$nombre_categoria,
  Soporte    = df_per_class$soporte_real,
  Gemma_F1   = sprintf("%.4f", df_per_class$gemma_f1),
  Flash35_F1 = sprintf("%.4f", df_per_class$f35_f1),
  Flash37_F1 = sprintf("%.4f", df_per_class$f37_f1),
  stringsAsFactors = FALSE
)

idx_b <- sum(df_per_class$componente_id == "b")
idx_d <- idx_b + sum(df_per_class$componente_id == "d")

tabla2_apa <- flextable(df_t2) %>%
  set_header_labels(
    Componente = "Componente CIF",
    Codigo     = "Código",
    Categoria  = "Categoría CIF (Core Set)",
    Soporte    = "Soporte Real",
    Gemma_F1   = "Gemma-4-31B (F1)",
    Flash35_F1 = "Flash 3.5 (F1)",
    Flash37_F1 = "Flash 3.7 (F1)"
  ) %>%
  merge_v(j = "Componente") %>%
  valign(j = "Componente", valign = "top") %>%
  italic(j = "Componente") %>%
  bold(j = "Codigo") %>%
  bold(part = "header") %>%
  align(j = 1:3, align = "left", part = "all") %>%
  align(j = 4:7, align = "center", part = "all") %>%
  border_remove() %>%
  hline_top(part = "header", border = border_main) %>%
  hline_bottom(part = "header", border = border_sub) %>%
  hline_bottom(part = "body", border = border_main) %>%
  hline(i = c(idx_b, idx_d), border = border_sub) %>%
  padding(padding.top = 2.5, padding.bottom = 2.5, padding.left = 4, padding.right = 4, part = "all") %>%
  fontsize(size = 8.5, part = "body") %>%
  fontsize(size = 9, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  autofit()

# ==============================================================================
# TABLA 3: COMPARATIVA SINTÉTICO (N=114) VS FISIOTERAPEUTAS (N=21)
# ==============================================================================
s35 <- res_syn[res_syn$modelo_id == "gemini_flash_35", ]
s37 <- if (any(res_syn$modelo_id == "gemini_flash_37")) res_syn[res_syn$modelo_id == "gemini_flash_37", ] else res_syn[res_syn$modelo_id == "gemini_flash_36", ]
sg  <- res_syn[res_syn$modelo_id == "gemma_31b", ]

f35_syn_fiab <- res_fiab$gemini_flash_35
f37_syn_fiab <- if (!is.null(res_fiab$gemini_flash_37)) res_fiab$gemini_flash_37 else res_fiab$gemini_flash_36
gemma_syn_fiab <- res_fiab$gemma_31b

df_t3 <- data.frame(
  Metrica = c(
    "Exact Match Ratio (EMR, %)",
    "Precisión Micro",
    "Sensibilidad / Recall Micro",
    "Micro-F1",
    "Macro-F1",
    "Weighted-F1",
    "Acuerdo Exacto Intra-Modelo (PAE, %)",
    "Coeficiente AC1 de Gwet",
    "Alfa de Krippendorff"
  ),
  Gemma_Sintetico = c(
    sprintf("%.2f%%", as.numeric(sg$metricas$emr_pct)),
    sprintf("%.4f", as.numeric(sg$metricas$micro$precision)),
    sprintf("%.4f", as.numeric(sg$metricas$micro$recall)),
    sprintf("%.4f", as.numeric(sg$metricas$micro$f1)),
    sprintf("%.4f", as.numeric(sg$metricas$macro$f1)),
    sprintf("%.4f", as.numeric(sg$metricas$weighted$f1)),
    sprintf("%.2f%%", as.numeric(gemma_syn_fiab$emr_pct)),
    sprintf("%.4f", as.numeric(gemma_syn_fiab$Gwet_AC1)),
    sprintf("%.4f", as.numeric(gemma_syn_fiab$Krippendorff_Alpha))
  ),
  Gemma_Humano = c(
    sprintf("%.2f%%", as.numeric(fg$desempeno$emr)),
    sprintf("%.4f", as.numeric(fg$desempeno$micro$p)),
    sprintf("%.4f", as.numeric(fg$desempeno$micro$r)),
    sprintf("%.4f", as.numeric(fg$desempeno$micro$f1)),
    sprintf("%.4f", as.numeric(fg$desempeno$macro$f1)),
    sprintf("%.4f", as.numeric(fg$desempeno$weighted$f1)),
    sprintf("%.2f%%", as.numeric(fg$fiabilidad$pae_pct)),
    sprintf("%.4f", as.numeric(fg$fiabilidad$ac1)),
    sprintf("%.4f", as.numeric(fg$fiabilidad$alpha))
  ),
  Gemma_Retencion = c(
    sprintf("%.1f%%", (as.numeric(fg$desempeno$emr) / as.numeric(sg$metricas$emr_pct)) * 100),
    sprintf("%.1f%%", (as.numeric(fg$desempeno$micro$p) / as.numeric(sg$metricas$micro$precision)) * 100),
    sprintf("%.1f%%", (as.numeric(fg$desempeno$micro$r) / as.numeric(sg$metricas$micro$recall)) * 100),
    sprintf("%.1f%%", (as.numeric(fg$desempeno$micro$f1) / as.numeric(sg$metricas$micro$f1)) * 100),
    sprintf("%.1f%%", (as.numeric(fg$desempeno$macro$f1) / as.numeric(sg$metricas$macro$f1)) * 100),
    sprintf("%.1f%%", (as.numeric(fg$desempeno$weighted$f1) / as.numeric(sg$metricas$weighted$f1)) * 100),
    sprintf("%.1f%%", (as.numeric(fg$fiabilidad$pae_pct) / as.numeric(gemma_syn_fiab$emr_pct)) * 100),
    sprintf("%.1f%%", (as.numeric(fg$fiabilidad$ac1) / as.numeric(gemma_syn_fiab$Gwet_AC1)) * 100),
    sprintf("%.1f%%", (as.numeric(fg$fiabilidad$alpha) / as.numeric(gemma_syn_fiab$Krippendorff_Alpha)) * 100)
  ),
  Flash35_Sintetico = c(
    sprintf("%.2f%%", as.numeric(s35$metricas$emr_pct)),
    sprintf("%.4f", as.numeric(s35$metricas$micro$precision)),
    sprintf("%.4f", as.numeric(s35$metricas$micro$recall)),
    sprintf("%.4f", as.numeric(s35$metricas$micro$f1)),
    sprintf("%.4f", as.numeric(s35$metricas$macro$f1)),
    sprintf("%.4f", as.numeric(s35$metricas$weighted$f1)),
    sprintf("%.2f%%", as.numeric(f35_syn_fiab$emr_pct)),
    sprintf("%.4f", as.numeric(f35_syn_fiab$Gwet_AC1)),
    sprintf("%.4f", as.numeric(f35_syn_fiab$Krippendorff_Alpha))
  ),
  Flash35_Humano = c(
    sprintf("%.2f%%", as.numeric(f35$desempeno$emr)),
    sprintf("%.4f", as.numeric(f35$desempeno$micro$p)),
    sprintf("%.4f", as.numeric(f35$desempeno$micro$r)),
    sprintf("%.4f", as.numeric(f35$desempeno$micro$f1)),
    sprintf("%.4f", as.numeric(f35$desempeno$macro$f1)),
    sprintf("%.4f", as.numeric(f35$desempeno$weighted$f1)),
    sprintf("%.2f%%", as.numeric(f35$fiabilidad$pae_pct)),
    sprintf("%.4f", as.numeric(f35$fiabilidad$ac1)),
    sprintf("%.4f", as.numeric(f35$fiabilidad$alpha))
  ),
  Flash35_Retencion = c(
    sprintf("%.1f%%", (as.numeric(f35$desempeno$emr) / as.numeric(s35$metricas$emr_pct)) * 100),
    sprintf("%.1f%%", (as.numeric(f35$desempeno$micro$p) / as.numeric(s35$metricas$micro$precision)) * 100),
    sprintf("%.1f%%", (as.numeric(f35$desempeno$micro$r) / as.numeric(s35$metricas$micro$recall)) * 100),
    sprintf("%.1f%%", (as.numeric(f35$desempeno$micro$f1) / as.numeric(s35$metricas$micro$f1)) * 100),
    sprintf("%.1f%%", (as.numeric(f35$desempeno$macro$f1) / as.numeric(s35$metricas$macro$f1)) * 100),
    sprintf("%.1f%%", (as.numeric(f35$desempeno$weighted$f1) / as.numeric(s35$metricas$weighted$f1)) * 100),
    sprintf("%.1f%%", (as.numeric(f35$fiabilidad$pae_pct) / as.numeric(f35_syn_fiab$emr_pct)) * 100),
    sprintf("%.1f%%", (as.numeric(f35$fiabilidad$ac1) / as.numeric(f35_syn_fiab$Gwet_AC1)) * 100),
    sprintf("%.1f%%", (as.numeric(f35$fiabilidad$alpha) / as.numeric(f35_syn_fiab$Krippendorff_Alpha)) * 100)
  ),
  Flash37_Sintetico = c(
    sprintf("%.2f%%", as.numeric(s37$metricas$emr_pct)),
    sprintf("%.4f", as.numeric(s37$metricas$micro$precision)),
    sprintf("%.4f", as.numeric(s37$metricas$micro$recall)),
    sprintf("%.4f", as.numeric(s37$metricas$micro$f1)),
    sprintf("%.4f", as.numeric(s37$metricas$macro$f1)),
    sprintf("%.4f", as.numeric(s37$metricas$weighted$f1)),
    sprintf("%.2f%%", as.numeric(f37_syn_fiab$emr_pct)),
    sprintf("%.4f", as.numeric(f37_syn_fiab$Gwet_AC1)),
    sprintf("%.4f", as.numeric(f37_syn_fiab$Krippendorff_Alpha))
  ),
  Flash37_Humano = c(
    sprintf("%.2f%%", as.numeric(f37$desempeno$emr)),
    sprintf("%.4f", as.numeric(f37$desempeno$micro$p)),
    sprintf("%.4f", as.numeric(f37$desempeno$micro$r)),
    sprintf("%.4f", as.numeric(f37$desempeno$micro$f1)),
    sprintf("%.4f", as.numeric(f37$desempeno$macro$f1)),
    sprintf("%.4f", as.numeric(f37$desempeno$weighted$f1)),
    sprintf("%.2f%%", as.numeric(f37$fiabilidad$pae_pct)),
    sprintf("%.4f", as.numeric(f37$fiabilidad$ac1)),
    sprintf("%.4f", as.numeric(f37$fiabilidad$alpha))
  ),
  Flash37_Retencion = c(
    sprintf("%.1f%%", (as.numeric(f37$desempeno$emr) / as.numeric(s37$metricas$emr_pct)) * 100),
    sprintf("%.1f%%", (as.numeric(f37$desempeno$micro$p) / as.numeric(s37$metricas$micro$precision)) * 100),
    sprintf("%.1f%%", (as.numeric(f37$desempeno$micro$r) / as.numeric(s37$metricas$micro$recall)) * 100),
    sprintf("%.1f%%", (as.numeric(f37$desempeno$micro$f1) / as.numeric(s37$metricas$micro$f1)) * 100),
    sprintf("%.1f%%", (as.numeric(f37$desempeno$macro$f1) / as.numeric(s37$metricas$macro$f1)) * 100),
    sprintf("%.1f%%", (as.numeric(f37$desempeno$weighted$f1) / as.numeric(s37$metricas$weighted$f1)) * 100),
    sprintf("%.1f%%", (as.numeric(f37$fiabilidad$pae_pct) / as.numeric(f37_syn_fiab$emr_pct)) * 100),
    sprintf("%.1f%%", (as.numeric(f37$fiabilidad$ac1) / as.numeric(f37_syn_fiab$Gwet_AC1)) * 100),
    sprintf("%.1f%%", (as.numeric(f37$fiabilidad$alpha) / as.numeric(f37_syn_fiab$Krippendorff_Alpha)) * 100)
  ),
  stringsAsFactors = FALSE
)

tabla3_apa <- flextable(df_t3) %>%
  set_header_labels(
    Metrica           = "Métrica Diagnóstica y Fiabilidad",
    Gemma_Sintetico   = "Gemma (Sint.)",
    Gemma_Humano      = "Gemma (Hum.)",
    Gemma_Retencion   = "Ret. (%)",
    Flash35_Sintetico = "Flash 3.5 (Sint.)",
    Flash35_Humano    = "Flash 3.5 (Hum.)",
    Flash35_Retencion = "Ret. (%)",
    Flash37_Sintetico = "Flash 3.7 (Sint.)",
    Flash37_Humano    = "Flash 3.7 (Hum.)",
    Flash37_Retencion = "Ret. (%)"
  ) %>%
  bold(part = "header") %>%
  align(j = 1, align = "left", part = "all") %>%
  align(j = 2:10, align = "center", part = "all") %>%
  border_remove() %>%
  hline_top(part = "header", border = border_main) %>%
  hline_bottom(part = "header", border = border_sub) %>%
  hline_bottom(part = "body", border = border_main) %>%
  hline(i = c(1, 4, 6), border = border_light) %>%
  padding(padding.top = 3, padding.bottom = 3, padding.left = 3, padding.right = 3, part = "all") %>%
  fontsize(size = 8, part = "body") %>%
  fontsize(size = 8.5, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  autofit()

doc <- read_docx() %>%
  body_add_par("Validación del Pipeline con Historias Clínicas de Fisioterapeutas: Tablas APA", style = "heading 1") %>%
  body_add_par("Tabla 1. Evaluación global del desempeño diagnóstico y fiabilidad intra-modelo ante historias clínicas de fisioterapeutas (N = 21).", style = "Normal") %>%
  body_add_flextable(tabla1_apa) %>%
  body_add_par("", style = "Normal") %>%
  body_add_par("Tabla 2. Auditoría detallada de clasificación F1 por categoría CIF en historias humanas.", style = "Normal") %>%
  body_add_flextable(tabla2_apa) %>%
  body_add_par("", style = "Normal") %>%
  body_add_par("Tabla 3. Comparativa de generalización del pipeline: Rendimiento ante corpus sintético (N = 114) versus corpus de fisioterapeutas (N = 21).", style = "Normal") %>%
  body_add_flextable(tabla3_apa)

print(doc, target = out_docx)
cat(" [OK] Documento de tablas APA generado con éxito en:", out_docx, "\n")
''', encoding='utf-8')

print('All 3 R scripts written successfully.')
