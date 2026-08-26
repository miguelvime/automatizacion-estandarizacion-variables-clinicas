# -*- coding: utf-8 -*-
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
    Gemma_31B = "Gemma-4-31B-it",
    Flash_35 = "Gemini Flash 3.5",
    Flash_37 = "Gemini Flash 3.7"
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
  "Gemma-4-31B-it", as.character(gemma$historias), sprintf("%d / %d", as.integer(gemma$emr_acuerdos), as.integer(gemma$historias)), sprintf("%.2f%%", as.numeric(gemma$emr_pct)), sprintf("%.4f%%", as.numeric(gemma$Po) * 100), sprintf("%.4f", as.numeric(gemma$Gwet_AC1)), sprintf("%.4f", as.numeric(gemma$Krippendorff_Alpha)),
  "Gemini Flash 3.5", as.character(f35$historias), sprintf("%d / %d", as.integer(f35$emr_acuerdos), as.integer(f35$historias)), sprintf("%.2f%%", as.numeric(f35$emr_pct)), sprintf("%.4f%%", as.numeric(f35$Po) * 100), sprintf("%.4f", as.numeric(f35$Gwet_AC1)), sprintf("%.4f", as.numeric(f35$Krippendorff_Alpha)),
  "Gemini Flash 3.7", as.character(f37$historias), sprintf("%d / %d", as.integer(f37$emr_acuerdos), as.integer(f37$historias)), sprintf("%.2f%%", as.numeric(f37$emr_pct)), sprintf("%.4f%%", as.numeric(f37$Po) * 100), sprintf("%.4f", as.numeric(f37$Gwet_AC1)), sprintf("%.4f", as.numeric(f37$Krippendorff_Alpha))
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
cat(" [OK] Documento exportado a:", ruta_salida_docx, "
")
