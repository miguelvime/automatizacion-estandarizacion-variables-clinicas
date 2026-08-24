# -*- coding: utf-8 -*-
# =============================================================================
# GENERACIÓN DE TABLA DE FIABILIDAD Y CONFIABILIDAD INTER-ITERACIONES EN DOCX
# ESTÁNDAR EDITORIAL APA / BOOKTABS (Skill: tfl-apa-tables)
# =============================================================================

suppressPackageStartupMessages({
  library(dplyr)
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

ruta_salida_docx <- file.path(tablas_dir, "tabla_fiabilidad_apa.docx")

border_main <- fp_border(color = "#222222", width = 1.5)
border_sub  <- fp_border(color = "#444444", width = 0.8)

# =============================================================================
# TABLA 1: MODELOS EN COLUMNAS, VARIABLES EN FILAS (TRANSPUESTA CON AGRUPACIÓN)
# =============================================================================
df_transpuesta <- tibble::tribble(
  ~Dimension, ~Metrica, ~Gemma_31B, ~Flash_35, ~Flash_36,
  "Corpus Clínico", "Historias Clínicas Evaluadas (N)", "114", "114", "114",
  "Corpus Clínico", "Iteraciones Independientes (K)", "3", "3", "3",
  "Corpus Clínico", "Espacio de Decisiones Binarias (114 × 3 × 27)", "9.234", "9.234", "9.234",
  
  "Acuerdo Multietiqueta", "Acuerdo Exacto Consensuado 3/3 (n / N)", "112 / 114", "112 / 114", "114 / 114",
  "Acuerdo Multietiqueta", "Exact Match Ratio (EMR %)", "98.25%", "98.25%", "100.00%",
  
  "Confiabilidad Ajustada", "Acuerdo Observado Po (%)", "99.9567%", "99.9567%", "100.0000%",
  "Confiabilidad Ajustada", "Coeficiente Gwet's AC1", "0.9994", "0.9994", "1.0000",
  "Confiabilidad Ajustada", "Alpha de Krippendorff (α)", "0.9983", "0.9983", "1.0000"
)

ft_transpuesta <- flextable(df_transpuesta) %>%
  set_header_labels(
    Dimension = "Dimensión",
    Metrica = "Métrica de Reproducibilidad",
    Gemma_31B = "Gemma-4-31B-it",
    Flash_35 = "Gemini Flash 3.5",
    Flash_36 = "Gemini Flash 3.6"
  ) %>%
  merge_v(j = "Dimension") %>%
  valign(j = "Dimension", valign = "top") %>%
  italic(j = "Dimension") %>%
  bold(part = "header") %>%
  bold(i = c(5, 7, 8), j = c("Metrica", "Gemma_31B", "Flash_35", "Flash_36")) %>%
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

# =============================================================================
# TABLA 2: MODELOS EN FILAS
# =============================================================================
df_modelos_filas <- tibble::tribble(
  ~Modelo, ~Historias, ~Acuerdo_Exacto, ~EMR_pct, ~Po_pct, ~Gwets_AC1, ~Krippendorff_alpha,
  "Gemma-4-31B-it", "114", "112 / 114", "98.25%", "99.9567%", "0.9994", "0.9983",
  "Gemini Flash 3.5", "114", "112 / 114", "98.25%", "99.9567%", "0.9994", "0.9983",
  "Gemini Flash 3.6", "114", "114 / 114", "100.00%", "100.0000%", "1.0000", "1.0000"
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
  width(j = 1, width = 1.6) %>%
  width(j = 2:7, width = 0.95) %>%
  set_caption(caption = "Tabla 2. Métricas de consistencia y confiabilidad inter-iteraciones por modelo LLM.")

doc <- read_docx() %>%
  body_add_par("Confiabilidad y Reproducibilidad Inter-Iteraciones de los Modelos LLM", style = "heading 1") %>%
  body_add_par("Evaluación del acuerdo intra-modelo a través de 3 iteraciones independientes bajo temperatura controlada (114 historias clínicas, espacio de 9.234 decisiones ontológicas).", style = "Normal") %>%
  body_add_par("", style = "Normal") %>%
  body_add_par("Formato Transpuesto (Modelos en Columnas)", style = "heading 2") %>%
  body_add_flextable(ft_transpuesta) %>%
  body_add_par("", style = "Normal") %>%
  body_add_par("", style = "Normal") %>%
  body_add_par("Formato Clásico (Modelos en Filas)", style = "heading 2") %>%
  body_add_flextable(ft_filas)

print(doc, target = ruta_salida_docx)

cat("===========================================================================\n")
cat(" [OK] Tablas de fiabilidad formateadas sin menciones de local o cloud\n")
cat(" [OK] Documento exportado a:", ruta_salida_docx, "\n")
cat("===========================================================================\n")
