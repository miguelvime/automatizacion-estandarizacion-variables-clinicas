
# F1 Score calculation: micro and macro
library(jsonlite)
library(tidyverse)

# Reading JSON and preparing df for calculation

codifier_output<-fromJSON("./data/test_data/test_codifier_output.json",flatten = TRUE)
codifier_output_no_text<- codifier_output |>
  select(id_code_combination,icf_codes,id_clinical_text,predicted_icf_codes)


confusion_matrix_per_clinical_text <- codifier_output_no_text |> 
  mutate(
    true_positive = map2_dbl(icf_codes, predicted_icf_codes, ~ length(intersect(.x, .y))),
    false_positive = map2_dbl(predicted_icf_codes, icf_codes, ~ length(setdiff(.x, .y))),
    false_negative = map2_dbl(icf_codes, predicted_icf_codes, ~ length(setdiff(.x, .y))),
  )
confusion_matrix_total<- confusion_matrix_per_clinical_text |> 
  summarise(
    total_true_positive = sum(true_positive),
    total_false_positive = sum(false_positive),
    total_false_negative = sum(false_negative))

  
micro_precision <- confusion_matrix_total$total_true_positive / (confusion_matrix_total$total_true_positive + confusion_matrix_total$total_false_positive)
micro_recall <- confusion_matrix_total$total_true_positive / (confusion_matrix_total$total_true_positive + confusion_matrix_total$total_false_negative)
micro_average_f1 <- 2* ((micro_precision * micro_recall) / (micro_precision + micro_recall))    

micro_average_metrics <- data.frame(micro_average_f1,micro_precision,micro_recall)

# F1 score per class

ground_truth_codes <- codifier_output_no_text |>
  select(id_clinical_text, icf_codes) |>
  unnest(cols = c(icf_codes)) |>
  rename(codigo = icf_codes) |>
  mutate(is_real = 1)

predicted_codes <- codifier_output_no_text |>
  select(id_clinical_text, predicted_icf_codes) |>
  unnest(cols = c(predicted_icf_codes)) |>
  rename(codigo = predicted_icf_codes) |>
  mutate(is_predicted = 1)

per_class_df <- full_join(ground_truth_codes, predicted_codes, by = c("id_clinical_text", "codigo")) |>
  replace_na(list(is_real = 0, is_predicted = 0)) |>
  group_by(codigo) |>
  summarise(
    true_positive = sum(is_real == 1 & is_predicted == 1),
    false_positive = sum(is_real == 0 & is_predicted == 1),
    false_negative = sum(is_real == 1 & is_predicted == 0),
    n_per_class = sum(is_real == 1),
    .groups = "drop"
  ) |>
  mutate(
    precision = if_else((true_positive + false_positive) == 0, 0, true_positive / (true_positive + false_positive)),
    recall    = if_else((true_positive + false_negative) == 0, 0, true_positive / (true_positive + false_negative)),
    f1_score  = if_else((precision + recall) == 0, 0, 2 * ((precision * recall) / (precision + recall))),
    n_total = sum(n_per_class)
  ) |>
  arrange(desc(f1_score)) 

macro_average_metrics <- per_class_df |> 
  mutate(
    macro_average_f1 = mean(f1_score),
    macro_average_precision = sum (precision) / nrow(per_class_df),
    macro_average_recall = sum (recall) / nrow(per_class_df)
  ) |> 
  select(macro_average_f1,macro_average_precision, macro_average_recall) |> 
  slice(1)

weighted_metrics <- per_class_df |> 
  mutate(
    weighted_f1 = sum(f1_score * n_per_class / n_total),
    weighted_precision = sum(precision * n_per_class / n_total),
    weighted_recall = sum (recall * n_per_class / n_total)) |> 
  select(weighted_f1,weighted_precision,weighted_recall) |> 
  slice(1)


per_class_metrics <- per_class_df |> 
  select(f1_score, precision, recall, n_per_class)

macro_average_metrics
weighted_metrics
micro_average_metrics
per_class_metrics

macro_average_metrics <- macro_average_metrics |> 
  rename(
    f1 = macro_average_f1,
    precision = macro_average_precision,
    recall = macro_average_recall)

weighted_metrics <- weighted_metrics |> 
  rename(
    f1 = weighted_f1,
    precision = weighted_precision,
    recall = weighted_recall
  )

micro_average_metrics <- micro_average_metrics |> 
  rename(
    f1 = micro_average_f1,
    precision = micro_precision,
    recall = micro_recall
  )

metrics<-t(data.frame (
  macro = t(macro_average_metrics),
  weighted =t(weighted_metrics),
  micro =t(micro_average_metrics)
))


metrics


#-------------------------------------------------------------------------------------------------------------#

#Improvements:
# -Confidence intervals

library(purrr)

# 1. Encapsular tu lógica actual en una función
calcular_todas_las_metricas <- function(df_datos) {
  
  confusion_matrix_per_clinical_text <- df_datos |> 
    mutate(
      true_positive = map2_dbl(icf_codes, predicted_icf_codes, ~ length(intersect(.x, .y))),
      false_positive = map2_dbl(predicted_icf_codes, icf_codes, ~ length(setdiff(.x, .y))),
      false_negative = map2_dbl(icf_codes, predicted_icf_codes, ~ length(setdiff(.x, .y)))
    )
  
  confusion_matrix_total <- confusion_matrix_per_clinical_text |> 
    summarise(
      total_true_positive = sum(true_positive),
      total_false_positive = sum(false_positive),
      total_false_negative = sum(false_negative)
    )

  micro_precision <- confusion_matrix_total$total_true_positive / (confusion_matrix_total$total_true_positive + confusion_matrix_total$total_false_positive)
  micro_recall <- confusion_matrix_total$total_true_positive / (confusion_matrix_total$total_true_positive + confusion_matrix_total$total_false_negative)
  micro_average_f1 <- 2* ((micro_precision * micro_recall) / (micro_precision + micro_recall))    

  micro_average_metrics <- data.frame(micro_average_f1, micro_precision, micro_recall)

  # F1 score per class
  ground_truth_codes <- df_datos |>
    select(id_clinical_text, icf_codes) |>
    unnest(cols = c(icf_codes)) |>
    rename(codigo = icf_codes) |>
    mutate(is_real = 1)

  predicted_codes <- df_datos |>
    select(id_clinical_text, predicted_icf_codes) |>
    unnest(cols = c(predicted_icf_codes)) |>
    rename(codigo = predicted_icf_codes) |>
    mutate(is_predicted = 1)

  per_class_df <- full_join(ground_truth_codes, predicted_codes, by = c("id_clinical_text", "codigo")) |>
    replace_na(list(is_real = 0, is_predicted = 0)) |>
    group_by(codigo) |>
    summarise(
      true_positive = sum(is_real == 1 & is_predicted == 1),
      false_positive = sum(is_real == 0 & is_predicted == 1),
      false_negative = sum(is_real == 1 & is_predicted == 0),
      n_per_class = sum(is_real == 1),
      .groups = "drop"
    ) |>
    mutate(
      precision = if_else((true_positive + false_positive) == 0, 0, true_positive / (true_positive + false_positive)),
      recall    = if_else((true_positive + false_negative) == 0, 0, true_positive / (true_positive + false_negative)),
      f1_score  = if_else((precision + recall) == 0, 0, 2 * ((precision * recall) / (precision + recall))),
      n_total = sum(n_per_class)
    ) |>
    arrange(desc(f1_score)) 

  macro_average_metrics <- per_class_df |> 
    mutate(
      macro_average_f1 = mean(f1_score, na.rm = TRUE),
      macro_average_precision = sum(precision) / nrow(per_class_df),
      macro_average_recall = sum(recall) / nrow(per_class_df)
    ) |> 
    select(macro_average_f1, macro_average_precision, macro_average_recall) |> 
    slice(1)

  weighted_metrics <- per_class_df |> 
    mutate(
      weighted_f1 = sum(f1_score * n_per_class / n_total, na.rm = TRUE),
      weighted_precision = sum(precision * n_per_class / n_total, na.rm = TRUE),
      weighted_recall = sum(recall * n_per_class / n_total, na.rm = TRUE)
    ) |> 
    select(weighted_f1, weighted_precision, weighted_recall) |> 
    slice(1)

  macro_average_metrics <- macro_average_metrics |> 
    rename(f1 = macro_average_f1, precision = macro_average_precision, recall = macro_average_recall)

  weighted_metrics <- weighted_metrics |> 
    rename(f1 = weighted_f1, precision = weighted_precision, recall = weighted_recall)

  micro_average_metrics <- micro_average_metrics |> 
    rename(f1 = micro_average_f1, precision = micro_precision, recall = micro_recall)

  # Devuelve un dataframe de 1 fila con las 3 métricas clave
  return(data.frame(
    micro_f1 = micro_average_metrics$f1,
    macro_f1 = macro_average_metrics$f1,
    weighted_f1 = weighted_metrics$f1
  ))
}

# 2. Configurar el Bootstrapping a nivel de documento
set.seed(2026) 
textos_unicos <- unique(codifier_output_no_text$id_clinical_text)
n_iteraciones <- 1000

# 3. Ejecutar el remuestreo empírico
resultados_boot <- map_dfr(1:n_iteraciones, function(i) {
  
  # Muestreo con reemplazo de los IDs de los textos
  ids_remuestreados <- sample(textos_unicos, replace = TRUE)
  
  # Reconstruir el dataframe temporal cruzando con los datos originales
  df_muestra <- tibble(id_clinical_text = ids_remuestreados) |> 
    left_join(codifier_output_no_text, by = "id_clinical_text", relationship = "many-to-many")
  
  # Calcular métricas para esta iteración
  calcular_todas_las_metricas(df_muestra)
})

# 4. Extraer los intervalos de confianza al 95%
intervalos_confianza <- resultados_boot |> 
  summarise(
    micro_f1_ci_lower = quantile(micro_f1, 0.025, na.rm = TRUE),
    micro_f1_ci_upper = quantile(micro_f1, 0.975, na.rm = TRUE),
    macro_f1_ci_lower = quantile(macro_f1, 0.025, na.rm = TRUE),
    macro_f1_ci_upper = quantile(macro_f1, 0.975, na.rm = TRUE),
    weighted_f1_ci_lower = quantile(weighted_f1, 0.025, na.rm = TRUE),
    weighted_f1_ci_upper = quantile(weighted_f1, 0.975, na.rm = TRUE)
  )

print(intervalos_confianza)

library(ggplot2)
library(tidyr)

# 1. Transformar los datos a formato largo para ggplot
resultados_largos <- resultados_boot |>
  pivot_longer(cols = everything(), names_to = "metrica", values_to = "f1_score")

# 2. Calcular los límites del intervalo y la media para pintarlos
limites_ci <- resultados_largos |>
  group_by(metrica) |>
  summarise(
    ci_lower = quantile(f1_score, 0.025, na.rm = TRUE),
    ci_upper = quantile(f1_score, 0.975, na.rm = TRUE),
    media = mean(f1_score, na.rm = TRUE)
  )

# 3. Crear el gráfico de densidad
ggplot(resultados_largos, aes(x = f1_score, fill = metrica)) +
  geom_density(alpha = 0.6) +
  geom_vline(data = limites_ci, aes(xintercept = ci_lower), linetype = "dashed", color = "black") +
  geom_vline(data = limites_ci, aes(xintercept = ci_upper), linetype = "dashed", color = "black") +
  geom_vline(data = limites_ci, aes(xintercept = media), linetype = "solid", color = "red") +
  facet_wrap(~metrica, scales = "free_y", ncol = 1) +
  theme_minimal() +
  labs(
    title = "Estabilidad del Bootstrap: Distribución de F1-Scores (1000 Iteraciones)",
    subtitle = "Línea roja = Media empírica | Líneas punteadas = Intervalo de confianza al 95%",
    x = "Valor F1-Score",
    y = "Densidad",
    fill = "Métrica"
  )
