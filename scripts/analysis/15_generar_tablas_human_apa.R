# -*- coding: utf-8 -*-
# ==============================================================================
# GENERADOR DE TABLAS EDITORIALES APA / BOOKTABS (SKILL TFL-APA-TABLES)
# VALIDACIÓN CON HISTORIAS CLÍNICAS DE FISIOTERAPEUTAS (N = 21)
# ==============================================================================

suppressPackageStartupMessages({
  library(flextable)
  library(officer)
  library(magrittr)
  library(jsonlite)
})

# 1. Definición de bordes estilo APA / Booktabs
border_main  <- fp_border(color = "#222222", width = 1.5)
border_sub   <- fp_border(color = "#444444", width = 0.8)
border_light <- fp_border(color = "#D0D0D0", width = 0.5)

# 2. Rutas
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
json_path  <- file.path(human_dir, "resumen_human_annotated.json")
csv_path   <- file.path(human_dir, "tabla_per_class_human.csv")
synth_path <- file.path(llm_dir, "resumen_f1_score.json")
out_docx   <- file.path(tablas_dir, "tablas_validacion_humana_apa.docx")

res_hum <- fromJSON(json_path)
res_syn <- fromJSON(synth_path)
df_per_class <- read.csv(csv_path, stringsAsFactors = FALSE, encoding = "UTF-8")

f35 <- res_hum$flash_35
f36 <- res_hum$flash_36
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
    "Espacio ontológico evaluado (N × 27)",
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
    "21", "567", "118", "5.62 ± 2.82", "Consenso estricto (3/3)",
    sprintf("%.2f%%", fg$fiabilidad$pae_pct),
    sprintf("%.2f%%", fg$fiabilidad$Po * 100),
    sprintf("%.4f", fg$fiabilidad$ac1),
    sprintf("%.4f", fg$fiabilidad$alpha),
    as.character(fg$desempeno$tp),
    as.character(fg$desempeno$fp),
    as.character(fg$desempeno$fn),
    sprintf("%.2f%% (%d/21)", fg$desempeno$emr, fg$desempeno$exact),
    sprintf("%.4f", fg$desempeno$micro$p),
    sprintf("%.4f", fg$desempeno$micro$r),
    sprintf("%.4f [%.4f, %.4f]", fg$desempeno$micro$f1, fg$ci_95$micro[1], fg$ci_95$micro[2]),
    sprintf("%.4f", fg$desempeno$macro$p),
    sprintf("%.4f", fg$desempeno$macro$r),
    sprintf("%.4f [%.4f, %.4f]", fg$desempeno$macro$f1, fg$ci_95$macro[1], fg$ci_95$macro[2]),
    sprintf("%.4f", fg$desempeno$weighted$p),
    sprintf("%.4f", fg$desempeno$weighted$r),
    sprintf("%.4f [%.4f, %.4f]", fg$desempeno$weighted$f1, fg$ci_95$weighted[1], fg$ci_95$weighted[2])
  ),
  Flash_35 = c(
    "21", "567", "118", "5.62 ± 2.82", "Consenso estricto (3/3)",
    sprintf("%.2f%%", f35$fiabilidad$pae_pct),
    sprintf("%.2f%%", f35$fiabilidad$Po * 100),
    sprintf("%.4f", f35$fiabilidad$ac1),
    sprintf("%.4f", f35$fiabilidad$alpha),
    as.character(f35$desempeno$tp),
    as.character(f35$desempeno$fp),
    as.character(f35$desempeno$fn),
    sprintf("%.2f%% (%d/21)", f35$desempeno$emr, f35$desempeno$exact),
    sprintf("%.4f", f35$desempeno$micro$p),
    sprintf("%.4f", f35$desempeno$micro$r),
    sprintf("%.4f [%.4f, %.4f]", f35$desempeno$micro$f1, f35$ci_95$micro[1], f35$ci_95$micro[2]),
    sprintf("%.4f", f35$desempeno$macro$p),
    sprintf("%.4f", f35$desempeno$macro$r),
    sprintf("%.4f [%.4f, %.4f]", f35$desempeno$macro$f1, f35$ci_95$macro[1], f35$ci_95$macro[2]),
    sprintf("%.4f", f35$desempeno$weighted$p),
    sprintf("%.4f", f35$desempeno$weighted$r),
    sprintf("%.4f [%.4f, %.4f]", f35$desempeno$weighted$f1, f35$ci_95$weighted[1], f35$ci_95$weighted[2])
  ),
  Flash_36 = c(
    "21", "567", "118", "5.62 ± 2.82", "Consenso estricto (3/3)",
    sprintf("%.2f%%", f36$fiabilidad$pae_pct),
    sprintf("%.2f%%", f36$fiabilidad$Po * 100),
    sprintf("%.4f", f36$fiabilidad$ac1),
    sprintf("%.4f", f36$fiabilidad$alpha),
    as.character(f36$desempeno$tp),
    as.character(f36$desempeno$fp),
    as.character(f36$desempeno$fn),
    sprintf("%.2f%% (%d/21)", f36$desempeno$emr, f36$desempeno$exact),
    sprintf("%.4f", f36$desempeno$micro$p),
    sprintf("%.4f", f36$desempeno$micro$r),
    sprintf("%.4f [%.4f, %.4f]", f36$desempeno$micro$f1, f36$ci_95$micro[1], f36$ci_95$micro[2]),
    sprintf("%.4f", f36$desempeno$macro$p),
    sprintf("%.4f", f36$desempeno$macro$r),
    sprintf("%.4f [%.4f, %.4f]", f36$desempeno$macro$f1, f36$ci_95$macro[1], f36$ci_95$macro[2]),
    sprintf("%.4f", f36$desempeno$weighted$p),
    sprintf("%.4f", f36$desempeno$weighted$r),
    sprintf("%.4f [%.4f, %.4f]", f36$desempeno$weighted$f1, f36$ci_95$weighted[1], f36$ci_95$weighted[2])
  ),
  stringsAsFactors = FALSE
)

tabla1_apa <- flextable(df_t1) %>%
  set_header_labels(
    Dimension = "Dimensión",
    Metrica   = "Métrica / Parámetro",
    Gemma_31B = "Gemma-4-31B-it (Local)",
    Flash_35  = "Gemini Flash 3.5 (Cloud)",
    Flash_36  = "Gemini Flash 3.6 (Cloud)"
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
  hline(i = c(5, 9, 13, 16, 19), border = border_light) %>%
  padding(padding.top = 3.5, padding.bottom = 3.5, padding.left = 5, padding.right = 5, part = "all") %>%
  fontsize(size = 9, part = "body") %>%
  fontsize(size = 9.5, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  autofit()

# ==============================================================================
# TABLA 2: AUDITORÍA PER CLASS POR COMPONENTE CIF (FORMATO LIMPIO APA)
# ==============================================================================
df_t2_clean <- data.frame(
  Componente = df_per_class$componente_nombre,
  Codigo     = df_per_class$codigo,
  Categoria  = df_per_class$nombre_categoria,
  Soporte    = df_per_class$soporte_real,
  Gemma_F1   = sprintf("%.2f", df_per_class$gemma_f1),
  Flash35_F1 = sprintf("%.2f", df_per_class$f35_f1),
  Flash36_F1 = sprintf("%.2f", df_per_class$f36_f1),
  stringsAsFactors = FALSE
)

tabla2_apa <- flextable(df_t2_clean) %>%
  set_header_labels(
    Componente = "Componente CIF",
    Codigo     = "Código",
    Categoria  = "Categoría CIF",
    Soporte    = "Soporte Real",
    Gemma_F1   = "Gemma 31B (F1)",
    Flash35_F1 = "Flash 3.5 (F1)",
    Flash36_F1 = "Flash 3.6 (F1)"
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
  hline(i = c(11, 22), border = border_sub) %>%
  padding(padding.top = 2.5, padding.bottom = 2.5, padding.left = 4, padding.right = 4, part = "all") %>%
  fontsize(size = 8.5, part = "body") %>%
  fontsize(size = 9, part = "header") %>%
  font(fontname = "Times New Roman", part = "all") %>%
  autofit()

# ==============================================================================
# TABLA 3: COMPARATIVA SINTÉTICO (N=114) VS FISIOTERAPEUTAS (N=21)
# ==============================================================================
s35 <- res_syn[res_syn$modelo_id == "gemini_flash_35", ]
s36 <- res_syn[res_syn$modelo_id == "gemini_flash_36", ]
sg  <- res_syn[res_syn$modelo_id == "gemma_31b", ]

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
    sprintf("%.2f%%", sg$metricas$emr_pct),
    sprintf("%.4f", sg$metricas$micro$precision),
    sprintf("%.4f", sg$metricas$micro$recall),
    sprintf("%.4f", sg$metricas$micro$f1),
    sprintf("%.4f", sg$metricas$macro$f1),
    sprintf("%.4f", sg$metricas$weighted$f1),
    "98.25%", "0.9994", "0.9983"
  ),
  Gemma_Humano = c(
    sprintf("%.2f%%", fg$desempeno$emr),
    sprintf("%.4f", fg$desempeno$micro$p),
    sprintf("%.4f", fg$desempeno$micro$r),
    sprintf("%.4f", fg$desempeno$micro$f1),
    sprintf("%.4f", fg$desempeno$macro$f1),
    sprintf("%.4f", fg$desempeno$weighted$f1),
    sprintf("%.2f%%", fg$fiabilidad$pae_pct),
    sprintf("%.4f", fg$fiabilidad$ac1),
    sprintf("%.4f", fg$fiabilidad$alpha)
  ),
  Gemma_Retencion = c(
    sprintf("%.1f%%", (fg$desempeno$emr / sg$metricas$emr_pct) * 100),
    sprintf("%.1f%%", (fg$desempeno$micro$p / sg$metricas$micro$precision) * 100),
    sprintf("%.1f%%", (fg$desempeno$micro$r / sg$metricas$micro$recall) * 100),
    sprintf("%.1f%%", (fg$desempeno$micro$f1 / sg$metricas$micro$f1) * 100),
    sprintf("%.1f%%", (fg$desempeno$macro$f1 / sg$metricas$macro$f1) * 100),
    sprintf("%.1f%%", (fg$desempeno$weighted$f1 / sg$metricas$weighted$f1) * 100),
    sprintf("%.1f%%", (fg$fiabilidad$pae_pct / 98.25) * 100),
    sprintf("%.1f%%", (fg$fiabilidad$ac1 / 0.9994) * 100),
    sprintf("%.1f%%", (fg$fiabilidad$alpha / 0.9983) * 100)
  ),
  Flash35_Sintetico = c(
    sprintf("%.2f%%", s35$metricas$emr_pct),
    sprintf("%.4f", s35$metricas$micro$precision),
    sprintf("%.4f", s35$metricas$micro$recall),
    sprintf("%.4f", s35$metricas$micro$f1),
    sprintf("%.4f", s35$metricas$macro$f1),
    sprintf("%.4f", s35$metricas$weighted$f1),
    "98.25%", "0.9994", "0.9983"
  ),
  Flash35_Humano = c(
    sprintf("%.2f%%", f35$desempeno$emr),
    sprintf("%.4f", f35$desempeno$micro$p),
    sprintf("%.4f", f35$desempeno$micro$r),
    sprintf("%.4f", f35$desempeno$micro$f1),
    sprintf("%.4f", f35$desempeno$macro$f1),
    sprintf("%.4f", f35$desempeno$weighted$f1),
    sprintf("%.2f%%", f35$fiabilidad$pae_pct),
    sprintf("%.4f", f35$fiabilidad$ac1),
    sprintf("%.4f", f35$fiabilidad$alpha)
  ),
  Flash35_Retencion = c(
    sprintf("%.1f%%", (f35$desempeno$emr / s35$metricas$emr_pct) * 100),
    sprintf("%.1f%%", (f35$desempeno$micro$p / s35$metricas$micro$precision) * 100),
    sprintf("%.1f%%", (f35$desempeno$micro$r / s35$metricas$micro$recall) * 100),
    sprintf("%.1f%%", (f35$desempeno$micro$f1 / s35$metricas$micro$f1) * 100),
    sprintf("%.1f%%", (f35$desempeno$macro$f1 / s35$metricas$macro$f1) * 100),
    sprintf("%.1f%%", (f35$desempeno$weighted$f1 / s35$metricas$weighted$f1) * 100),
    sprintf("%.1f%%", (f35$fiabilidad$pae_pct / 98.25) * 100),
    sprintf("%.1f%%", (f35$fiabilidad$ac1 / 0.9994) * 100),
    sprintf("%.1f%%", (f35$fiabilidad$alpha / 0.9983) * 100)
  ),
  Flash36_Sintetico = c(
    sprintf("%.2f%%", s36$metricas$emr_pct),
    sprintf("%.4f", s36$metricas$micro$precision),
    sprintf("%.4f", s36$metricas$micro$recall),
    sprintf("%.4f", s36$metricas$micro$f1),
    sprintf("%.4f", s36$metricas$macro$f1),
    sprintf("%.4f", s36$metricas$weighted$f1),
    "100.00%", "1.0000", "1.0000"
  ),
  Flash36_Humano = c(
    sprintf("%.2f%%", f36$desempeno$emr),
    sprintf("%.4f", f36$desempeno$micro$p),
    sprintf("%.4f", f36$desempeno$micro$r),
    sprintf("%.4f", f36$desempeno$micro$f1),
    sprintf("%.4f", f36$desempeno$macro$f1),
    sprintf("%.4f", f36$desempeno$weighted$f1),
    sprintf("%.2f%%", f36$fiabilidad$pae_pct),
    sprintf("%.4f", f36$fiabilidad$ac1),
    sprintf("%.4f", f36$fiabilidad$alpha)
  ),
  Flash36_Retencion = c(
    sprintf("%.1f%%", (f36$desempeno$emr / s36$metricas$emr_pct) * 100),
    sprintf("%.1f%%", (f36$desempeno$micro$p / s36$metricas$micro$precision) * 100),
    sprintf("%.1f%%", (f36$desempeno$micro$r / s36$metricas$micro$recall) * 100),
    sprintf("%.1f%%", (f36$desempeno$micro$f1 / s36$metricas$micro$f1) * 100),
    sprintf("%.1f%%", (f36$desempeno$macro$f1 / s36$metricas$macro$f1) * 100),
    sprintf("%.1f%%", (f36$desempeno$weighted$f1 / s36$metricas$weighted$f1) * 100),
    sprintf("%.1f%%", (f36$fiabilidad$pae_pct / 100.0) * 100),
    sprintf("%.1f%%", (f36$fiabilidad$ac1 / 1.0) * 100),
    sprintf("%.1f%%", (f36$fiabilidad$alpha / 1.0) * 100)
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
    Flash36_Sintetico = "Flash 3.6 (Sint.)",
    Flash36_Humano    = "Flash 3.6 (Hum.)",
    Flash36_Retencion = "Ret. (%)"
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

# ==============================================================================
# GUARDAR DOCUMENTO DE TABLAS APA EN WORD (.DOCX)
# ==============================================================================
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
