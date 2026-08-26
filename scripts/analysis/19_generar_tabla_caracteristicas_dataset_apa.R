# -*- coding: utf-8 -*-
# =============================================================================
# CARACTERÍSTICAS DEL CONJUNTO DE DATOS (APARTADO 5.3)
# Skill: tfl-apa-tables (flextable + officer en R)
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

tablas_dir <- file.path(base_dir, "results", "TFL", "tablas")
dir.create(tablas_dir, showWarnings = FALSE, recursive = TRUE)

ruta_docx <- file.path(tablas_dir, "tabla_caracteristicas_dataset_apa.docx")

# 1. Definir bordes estándar APA / Booktabs
border_main <- fp_border(color = "#222222", width = 1.5)
border_sub  <- fp_border(color = "#444444", width = 0.8)

# 2. Datos exactos del conjunto de datos reparado (Apartado 5.3)
df_caract <- tibble::tribble(
  ~Variable, ~Valor,
  "Textos clínicos (N)", "114",
  "Códigos ICF extraídos (n)", "465",
  "Códigos ICF únicos identificados (n)", "24",
  "Códigos por texto clínico (Media ± DE)", "4.08 ± 1.48",
  "Códigos por texto clínico (Mediana)", "4.0"
)

# 3. Construir la flextable siguiendo la skill tfl-apa-tables
ft <- flextable(df_caract) %>%
  set_header_labels(
    Variable = "Variable",
    Valor    = "Valor"
  ) %>%
  bold(part = "header") %>%
  # Alineación: Columna 1 a la izquierda, Columna 2 centrada
  align(j = 1, align = "left", part = "all") %>%
  align(j = 2, align = "center", part = "all") %>%
  # Cero bordes verticales y jerarquía horizontal APA
  border_remove() %>%
  hline_top(part = "header", border = border_main) %>%
  hline_bottom(part = "header", border = border_sub) %>%
  hline_bottom(part = "body", border = border_main) %>%
  # Espaciado interno y tipografía Times New Roman
  padding(padding.top = 5, padding.bottom = 5, padding.left = 8, padding.right = 8, part = "all") %>%
  fontsize(size = 9.5, part = "body") %>%
  fontsize(size = 10.0, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  # Anchos de columna equilibrados para página Word
  width(j = 1, width = 3.6) %>%
  width(j = 2, width = 1.6)

# 4. Crear el documento Word con formato editorial APA listo para copiar y pegar
doc <- read_docx() %>%
  body_add_par("Apartado 5.3: Características del conjunto de datos", style = "heading 1") %>%
  body_add_par("Tabla . Características métricas del conjunto de datos sintético generado.", style = "Normal") %>%
  body_add_flextable(ft) %>%
  body_add_par("Nota. DE: Desviación estándar. ICF: Clasificación Internacional del Funcionamiento, de la Discapacidad y de la Salud (CIF / OMS).", style = "Normal")

print(doc, target = ruta_docx)

cat("===========================================================================\n")
cat(" [OK] Tabla 5.3 (Características del dataset) guardada en:\n")
cat("      -", ruta_docx, "\n")
cat("===========================================================================\n")
