# -*- coding: utf-8 -*-
# =============================================================================
# GENERACIÓN DE TABLAS DE DESEMPEÑO DIAGNÓSTICO EN DOCX (ESTILO APA / BOOKTABS)
# Skill: tfl-apa-tables | Skill: clean-copy-paste-word
# =============================================================================

suppressPackageStartupMessages({
  library(jsonlite)
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

ruta_json <- file.path(llm_dir, "resumen_f1_score.json")
ruta_salida_docx <- file.path(tablas_dir, "tabla_desempeno_apa.docx")

if (!file.exists(ruta_json)) {
  stop(paste("No se encontró el archivo JSON en:", ruta_json))
}

datos_json <- fromJSON(ruta_json, simplifyDataFrame = FALSE)

gemma <- datos_json[[1]]
g35 <- datos_json[[2]]
g36 <- datos_json[[3]]

border_main <- fp_border(color = "#222222", width = 1.5)
border_sub  <- fp_border(color = "#444444", width = 0.8)

# =============================================================================
# TABLA 1: DESEMPEÑO GLOBAL Y MÉTRICAS MULTIETIQUETA (ESTILO BOOKTABS)
# =============================================================================
df_global <- tibble::tribble(
  ~Dimension, ~Metrica, ~Gemma_31B, ~Flash_35, ~Flash_37,
  "Corpus Clínico", "Historias evaluadas (N)", "114", "114", "114",
  "Corpus Clínico", "Espacio ontológico (114 × 24)", "2.736", "2.736", "2.736",
  "Corpus Clínico", "Instancias CIF reales (Soporte)", "465", "465", "465",
  "Corpus Clínico", "Consenso inter-iteraciones", "Estricto (3/3)", "Estricto (3/3)", "Estricto (3/3)",
  
  "Matriz de Confusión", "Verdaderos Positivos (TP)", as.character(gemma$metricas$confusion_global$tp), as.character(g35$metricas$confusion_global$tp), as.character(g36$metricas$confusion_global$tp),
  "Matriz de Confusión", "Falsos Positivos (FP / Alucinación)", as.character(gemma$metricas$confusion_global$fp), as.character(g35$metricas$confusion_global$fp), as.character(g36$metricas$confusion_global$fp),
  "Matriz de Confusión", "Falsos Negativos (FN / Omisión)", as.character(gemma$metricas$confusion_global$fn), as.character(g35$metricas$confusion_global$fn), as.character(g36$metricas$confusion_global$fn),
  "Matriz de Confusión", "Exact Match Ratio (EMR n / N)", sprintf("%d/114", gemma$metricas$exact_matches_n), sprintf("%d/114", g35$metricas$exact_matches_n), sprintf("%d/114", g36$metricas$exact_matches_n),
  "Matriz de Confusión", "Exact Match Ratio (EMR %)", sprintf("%.2f%%", gemma$metricas$emr_pct), sprintf("%.2f%%", g35$metricas$emr_pct), sprintf("%.2f%%", g36$metricas$emr_pct),
  
  "Nivel Micro", "Precisión Micro", sprintf("%.4f", gemma$metricas$micro$precision), sprintf("%.4f", g35$metricas$micro$precision), sprintf("%.4f", g36$metricas$micro$precision),
  "Nivel Micro", "Recall Micro (Sensibilidad)", sprintf("%.4f", gemma$metricas$micro$recall), sprintf("%.4f", g35$metricas$micro$recall), sprintf("%.4f", g36$metricas$micro$recall),
  "Nivel Micro", "Micro-F1 [IC 95% Bootstrap]", sprintf("%.4f [%.3f, %.3f]", gemma$metricas$micro$f1, gemma$ci_95$micro_f1[[1]], gemma$ci_95$micro_f1[[2]]), sprintf("%.4f [%.3f, %.3f]", g35$metricas$micro$f1, g35$ci_95$micro_f1[[1]], g35$ci_95$micro_f1[[2]]), sprintf("%.4f [%.3f, %.3f]", g36$metricas$micro$f1, g36$ci_95$micro_f1[[1]], g36$ci_95$micro_f1[[2]]),
  
  "Nivel Macro", "Precisión Macro", sprintf("%.4f", gemma$metricas$macro$precision), sprintf("%.4f", g35$metricas$macro$precision), sprintf("%.4f", g36$metricas$macro$precision),
  "Nivel Macro", "Recall Macro", sprintf("%.4f", gemma$metricas$macro$recall), sprintf("%.4f", g35$metricas$macro$recall), sprintf("%.4f", g36$metricas$macro$recall),
  "Nivel Macro", "Macro-F1 [IC 95% Bootstrap]", sprintf("%.4f [%.3f, %.3f]", gemma$metricas$macro$f1, gemma$ci_95$macro_f1[[1]], gemma$ci_95$macro_f1[[2]]), sprintf("%.4f [%.3f, %.3f]", g35$metricas$macro$f1, g35$ci_95$macro_f1[[1]], g35$ci_95$macro_f1[[2]]), sprintf("%.4f [%.3f, %.3f]", g36$metricas$macro$f1, g36$ci_95$macro_f1[[1]], g36$ci_95$macro_f1[[2]]),
  
  "Nivel Weighted", "Precisión Weighted", sprintf("%.4f", gemma$metricas$weighted$precision), sprintf("%.4f", g35$metricas$weighted$precision), sprintf("%.4f", g36$metricas$weighted$precision),
  "Nivel Weighted", "Recall Weighted", sprintf("%.4f", gemma$metricas$weighted$recall), sprintf("%.4f", g35$metricas$weighted$recall), sprintf("%.4f", g36$metricas$weighted$recall),
  "Nivel Weighted", "Weighted-F1 [IC 95% Bootstrap]", sprintf("%.4f [%.3f, %.3f]", gemma$metricas$weighted$f1, gemma$ci_95$weighted_f1[[1]], gemma$ci_95$weighted_f1[[2]]), sprintf("%.4f [%.3f, %.3f]", g35$metricas$weighted$f1, g35$ci_95$weighted_f1[[1]], g35$ci_95$weighted_f1[[2]]), sprintf("%.4f [%.3f, %.3f]", g36$metricas$weighted$f1, g36$ci_95$weighted_f1[[1]], g36$ci_95$weighted_f1[[2]])
)

ft1 <- flextable(df_global) %>%
  set_header_labels(
    Dimension = "Dimensión",
    Metrica = "Métrica / Parámetro",
    Gemma_31B = "Gemma-4-31B-it",
    Flash_35 = "Gemini Flash 3.5",
    Flash_37 = "Gemini Flash 3.7"
  ) %>%
  merge_v(j = "Dimension") %>%
  valign(j = "Dimension", valign = "top") %>%
  italic(j = "Dimension") %>%
  bold(part = "header") %>%
  bold(i = c(9, 12, 15, 18), j = c("Metrica", "Gemma_31B", "Flash_35", "Flash_37")) %>%
  align(j = 1:2, align = "left", part = "all") %>%
  align(j = 3:5, align = "center", part = "all") %>%
  border_remove() %>%
  hline_top(part = "header", border = border_main) %>%
  hline_bottom(part = "header", border = border_sub) %>%
  hline_bottom(part = "body", border = border_main) %>%
  hline(i = c(4, 9, 12, 15), border = border_sub) %>%
  padding(padding.top = 4, padding.bottom = 4, padding.left = 6, padding.right = 6, part = "all") %>%
  fontsize(size = 9.5, part = "all") %>%
  fontsize(size = 10, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  width(j = 1, width = 1.3) %>%
  width(j = 2, width = 2.1) %>%
  width(j = 3:5, width = 1.25) %>%
  set_caption(caption = "Tabla 1. Evaluación global de desempeño diagnóstico y validez multietiqueta según la CIF.")

# =============================================================================
# TABLA 2: AUDITORÍA PER CLASS AGRUPADA POR COMPONENTE CIF (b, d, e)
# =============================================================================
gemma_clases <- gemma$metricas$por_clase
g35_clases <- g35$metricas$por_clase
g36_clases <- g36$metricas$por_clase

codigos <- sort(names(gemma_clases))

filas_per_class <- list()
for (c in codigos) {
  letra <- substr(c, 1, 1)
  comp <- switch(letra,
    "b" = "Funciones Corporales (b)",
    "d" = "Actividades y Participación (d)",
    "e" = "Factores Ambientales (e)",
    "Otro"
  )
  nom <- gemma_clases[[c]]$nombre
  sup <- gemma_clases[[c]]$soporte
  
  f1_gem <- sprintf("%.4f", gemma_clases[[c]]$f1)
  f1_35 <- sprintf("%.4f", g35_clases[[c]]$f1)
  f1_36 <- sprintf("%.4f", g36_clases[[c]]$f1)
  
  filas_per_class[[length(filas_per_class) + 1]] <- list(
    Componente = comp,
    Codigo = c,
    Categoria = nom,
    Soporte = as.integer(sup),
    Gemma_F1 = f1_gem,
    Flash_35_F1 = f1_35,
    Flash_37_F1 = f1_36
  )
}

df_class <- bind_rows(filas_per_class)

idx_b_end <- sum(df_class$Componente == "Funciones Corporales (b)")
idx_d_end <- idx_b_end + sum(df_class$Componente == "Actividades y Participación (d)")

ft2 <- flextable(df_class) %>%
  set_header_labels(
    Componente = "Componente CIF",
    Codigo = "Código",
    Categoria = "Categoría CIF (Core Set Dolor Crónico)",
    Soporte = "Soporte (GT)",
    Gemma_F1 = "Gemma-4-31B-it (F1)",
    Flash_35_F1 = "Gemini Flash 3.5 (F1)",
    Flash_37_F1 = "Gemini Flash 3.7 (F1)"
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
  hline(i = c(idx_b_end, idx_d_end), border = border_sub) %>%
  padding(padding.top = 3, padding.bottom = 3, padding.left = 5, padding.right = 5, part = "all") %>%
  fontsize(size = 9, part = "all") %>%
  fontsize(size = 9.5, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  width(j = 1, width = 1.6) %>%
  width(j = 2, width = 0.6) %>%
  width(j = 3, width = 2.4) %>%
  width(j = 4, width = 0.7) %>%
  width(j = 5:7, width = 0.95) %>%
  set_caption(caption = "Tabla 2. Auditoría detallada del F1-Score en las 24 categorías CIF del Core Set de Dolor Crónico.")

# Exportar a documento Word
doc <- read_docx() %>%
  body_add_par("Desempeño Diagnóstico en la Codificación CIF Automatizada", style = "heading 1") %>%
  body_add_par("Evaluación comparativa de modelos LLM bajo consenso estricto (3/3) frente al Ground Truth (114 historias clínicas, Core Set CIF de dolor crónico con 24 categorías).", style = "Normal") %>%
  body_add_par("", style = "Normal") %>%
  body_add_flextable(ft1) %>%
  body_add_par("", style = "Normal") %>%
  body_add_par("", style = "Normal") %>%
  body_add_flextable(ft2)

print(doc, target = ruta_salida_docx)

cat("===========================================================================\n")
cat(" [OK] Tablas generadas en formato APA sin menciones de local o cloud\n")
cat(" [OK] Documento exportado a:", ruta_salida_docx, "\n")
cat("===========================================================================\n")
