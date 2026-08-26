# -*- coding: utf-8 -*-
# =============================================================================
# TABLA APA: ANÁLISIS DE SENSIBILIDAD POR ABLACIÓN DE LA CLASE DOMINANTE
# Skill: tfl-apa-tables | Skill: clean-copy-paste-word
# =============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(flextable)
  library(officer)
  library(magrittr)
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

data_dir    <- file.path(base_dir, "data")
results_dir <- file.path(base_dir, "results")
llm_dir     <- file.path(results_dir, "llm_text")
human_dir   <- file.path(results_dir, "human_text")
tfl_dir     <- file.path(results_dir, "TFL")
tablas_dir  <- file.path(tfl_dir, "tablas")
figuras_dir <- file.path(tfl_dir, "figuras")
informes_dir <- file.path(tfl_dir, "informes")

ruta_csv <- file.path(tablas_dir, "tabla_sensibilidad_ablacion.csv")
ruta_docx <- file.path(tablas_dir, "tabla_sensibilidad_ablacion_apa.docx")

df_datos <- read_csv(ruta_csv, show_col_types = FALSE)

# Definir bordes estilo APA / Booktabs
border_main <- fp_border(color = "#222222", width = 1.5)
border_sub  <- fp_border(color = "#444444", width = 0.8)
border_light <- fp_border(color = "#D0D0D0", width = 0.5)

ft <- flextable(df_datos) %>%
  set_header_labels(
    `Dimensión` = "Dimensión",
    `Métrica / Parámetro` = "Métrica / Parámetro",
    `Gemma-4-31B-it` = "Gemma-4-31B-it",
    `Gemini Flash 3.5` = "Gemini Flash 3.5",
    `Gemini Flash 3.7` = "Gemini Flash 3.7"
  ) %>%
  # 1. Fusión vertical de la primera columna (Dimensión)
  merge_v(j = 1) %>%
  valign(j = 1, valign = "top") %>%
  italic(j = 1) %>%
  bold(part = "header") %>%
  # 2. Alineaciones: texto a la izquierda, métricas al centro
  align(j = 1:2, align = "left", part = "all") %>%
  align(j = 3:5, align = "center", part = "all") %>%
  # 3. Cero líneas verticales y jerarquía horizontal
  border_remove() %>%
  hline_top(part = "header", border = border_main) %>%
  hline_bottom(part = "header", border = border_sub) %>%
  hline_bottom(part = "body", border = border_main) %>%
  # Líneas de separación entre bloques conceptuales
  hline(i = c(3, 8, 13, 17), border = border_sub) %>%
  # 4. Tipografía y espaciado editorial
  padding(padding.top = 4, padding.bottom = 4, padding.left = 6, padding.right = 6, part = "all") %>%
  fontsize(size = 9.0, part = "all") %>%
  fontsize(size = 9.5, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  autofit()

doc <- read_docx() %>%
  body_add_par("Tabla . Análisis de Sensibilidad y Ablación de la Categoría Dominante (b280)", style = "heading 2") %>%
  body_add_par("Evaluación comparativa del rendimiento diagnóstico en los tres modelos evaluados antes y después de excluir el código de dolor (b280).", style = "Normal") %>%
  body_add_flextable(ft) %>%
  body_add_par("Nota. N = 114 historias clínicas. La tasa de retención se define como [Métrica (Sin b280) / Métrica (Con b280)] × 100.", style = "Normal")

print(doc, target = ruta_docx)
cat("[+] Documento Word APA generado exitosamente en:", ruta_docx, "\n")
