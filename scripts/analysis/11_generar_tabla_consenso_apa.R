# -*- coding: utf-8 -*-
# =============================================================================
# EVALUACIÓN DE EFICIENCIA OPERATIVA: ESTRATEGIAS DE CONSENSO (1x vs 3x)
# Skill: tfl-apa-tables (flextable + officer)
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

ruta_docx <- file.path(tablas_dir, "tabla_estrategias_consenso_apa.docx")

border_main <- fp_border(color = "#222222", width = 1.5)
border_sub  <- fp_border(color = "#444444", width = 0.8)

# Datos de evaluación comparativa de estrategias
df_estrategias <- tibble::tribble(
  ~Regimen, ~Estrategia, ~Coste_Latencia, ~Gemma_F1, ~Gemma_EMR, ~Flash35_F1, ~Flash35_EMR, ~Flash36_F1, ~Flash36_EMR,
  "Pase Único (K=1)", "Iteración 1 (Pase Primario)", "1x (Óptimo)", "0.9699", "83.33%", "0.9709", "84.21%", "0.9709", "84.21%",
  "Pase Único (K=1)", "Iteración 2 (Segunda Corrida)", "1x", "0.9688", "82.46%", "0.9709", "84.21%", "0.9709", "84.21%",
  "Pase Único (K=1)", "Iteración 3 (Tercera Corrida)", "1x", "0.9677", "81.58%", "0.9709", "84.21%", "0.9709", "84.21%",
  
  "Multi-Pase (K=3)", "Consenso Estricto (3/3 Unánime)", "3x", "0.9688", "82.46%", "0.9720", "85.09%", "0.9709", "84.21%",
  "Multi-Pase (K=3)", "Voto Mayoritario (≥ 2/3)", "3x", "0.9688", "82.46%", "0.9709", "84.21%", "0.9709", "84.21%",
  "Multi-Pase (K=3)", "Unión / Sensibilidad (≥ 1/3)", "3x", "0.9689", "82.46%", "0.9699", "83.33%", "0.9709", "84.21%"
)

ft <- flextable(df_estrategias) %>%
  set_header_labels(
    Regimen = "Régimen de Inferencia",
    Estrategia = "Estrategia de Decisión",
    Coste_Latencia = "Coste Relativo",
    Gemma_F1 = "Gemma (F1)",
    Gemma_EMR = "Gemma (EMR)",
    Flash35_F1 = "Flash 3.5 (F1)",
    Flash35_EMR = "Flash 3.5 (EMR)",
    Flash36_F1 = "Flash 3.6 (F1)",
    Flash36_EMR = "Flash 3.6 (EMR)"
  ) %>%
  merge_v(j = "Regimen") %>%
  valign(j = "Regimen", valign = "top") %>%
  italic(j = "Regimen") %>%
  bold(i = c(1, 4), j = c("Estrategia", "Gemma_F1", "Flash35_F1", "Flash36_F1")) %>%
  bold(part = "header") %>%
  align(j = 1:2, align = "left", part = "all") %>%
  align(j = 3:9, align = "center", part = "all") %>%
  border_remove() %>%
  hline_top(part = "header", border = border_main) %>%
  hline_bottom(part = "header", border = border_sub) %>%
  hline_bottom(part = "body", border = border_main) %>%
  hline(i = 3, border = border_sub) %>%
  padding(padding.top = 4, padding.bottom = 4, padding.left = 5, padding.right = 5, part = "all") %>%
  fontsize(size = 9.0, part = "all") %>%
  fontsize(size = 9.5, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  width(j = 1, width = 1.3) %>%
  width(j = 2, width = 2.0) %>%
  width(j = 3, width = 0.8) %>%
  width(j = 4:9, width = 0.65) %>%
  set_caption(caption = "Tabla. Análisis de coste-efectividad y rendimiento diagnóstico según la estrategia de consenso (K=1 vs K=3).")

doc <- read_docx() %>%
  body_add_par("Eficiencia Operativa y Estrategias de Inferencia (Pase Único vs Consenso Multi-Pase)", style = "heading 1") %>%
  body_add_par("Comparativa de exactitud diagnóstica (Micro-F1 y EMR) frente al coste computacional y latencia en historias clínicas.", style = "Normal") %>%
  body_add_par("", style = "Normal") %>%
  body_add_flextable(ft)

print(doc, target = ruta_docx)

cat("===========================================================================\n")
cat(" [OK] Tabla de consenso guardada en:", ruta_docx, "\n")
cat("===========================================================================\n")
