# Instalación del paquete específico para el estadístico de Gwet
# install.packages("irrCAC")
# install.packages("tidyr")
# install.packages("dplyr")

library(irrCAC)
library(dplyr)
library(tidyr)

# 1. Definición de parámetros 
set.seed(123) # Semilla fija para reproducir la misma "paradoja"
pacientes_id <- paste0("P", 1:5)
iteraciones_llm <- paste0("Iter_", 1:5)
codigos_cif <- c("b280", "d430", "d760", "d770", "d920", 
                 "b710", "b730", "d410", "d420", "d440", 
                 "d450", "d840", "d850", "e110", "e120")

datos_largo <- expand.grid(
  Paciente = pacientes_id,
  Codigo = codigos_cif,
  Iteracion = iteraciones_llm
)

# 2. Simulación de Inferencia Altamente Desbalanceada
# Simulamos que el LLM casi siempre dice "0" (Ausente) para replicar 
# el entorno real de un conjunto de datos clínicos.
datos_largo$Prediccion <- sample(
  c(0, 1), 
  size = nrow(datos_largo), 
  replace = TRUE, 
  prob = c(0.85, 0.15) 
)

# =====================================================================
# TRANSFORMACIÓN MATRICIAL PARA GWET AC1
# =====================================================================

# El paquete irrCAC necesita: Filas = Sujetos (75) | Columnas = Evaluadores (5)
datos_ac1 <- datos_largo %>%
  mutate(Sujeto_Evaluado = paste(Paciente, Codigo, sep = "_")) %>%
  select(Sujeto_Evaluado, Iteracion, Prediccion) %>%
  pivot_wider(names_from = Iteracion, values_from = Prediccion)

# Eliminamos la columna de texto para dejar una matriz numérica pura (75 x 5)
matriz_ac1 <- datos_ac1 %>% select(-Sujeto_Evaluado)

# =====================================================================
# CÁLCULO DEL ESTADÍSTICO AC1 Y COMPARATIVA
# =====================================================================

# Calculamos Gwet's AC1
# El argumento weights = "unweighted" es necesario para variables nominales dicotómicas
resultado_ac1 <- gwet.ac1.raw(matriz_ac1, weights = "unweighted")

cat("\n--- RESULTADO AC1 DE GWET GLOBAL ---\n")
# El objeto devuelve múltiples valores, extraemos la estimación y el intervalo de confianza
print(resultado_ac1$est)

# Para demostrar empíricamente el problema, mostramos también el índice de porcentaje de acuerdo bruto
acuerdo_absoluto <- pa.coeff.raw(matriz_ac1)$est
cat("\n--- ACUERDO ABSOLUTO (BRUTO) ---\n")
print(acuerdo_absoluto)