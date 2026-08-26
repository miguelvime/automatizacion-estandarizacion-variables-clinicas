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
dir.create(tablas_dir, showWarnings = FALSE, recursive = TRUE)

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

cat(" [OK] Tabla 5.3 generada con formato tfl-apa-tables en:\n")
cat("      -", ruta_docx_apartado_53, "\n")
