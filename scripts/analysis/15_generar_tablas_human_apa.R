# -*- coding: utf-8 -*-
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
    Gemma_31B = "Gemma-4-31B-it",
    Flash_35  = "Gemini Flash 3.5",
    Flash_37  = "Gemini Flash 3.7"
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
cat(" [OK] Documento de tablas APA generado con éxito en:", out_docx, "
")
