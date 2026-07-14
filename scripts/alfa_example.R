# Instalar paquetes necesarios si no están instalados
# install.packages("irr")
# install.packages("tidyverse")

library(dplyr)
library(tidyr)
library(irr)

# 1. Definición de los parámetros del experimento sintético
set.seed(42) # Semilla para reproducibilidad de la prueba
pacientes_id <- paste0("P", 1:5)
iteraciones_llm <- paste0("Iter_", 1:5)
codigos_cif <- c("b280", "d430", "d760", "d770", "d920", 
                 "b710", "b730", "d410", "d420", "d440", 
                 "d450", "d840", "d850", "e110", "e120") # Tus 15 códigos

# 2. Generación del Data Frame (Formato Largo)
# Este es el esquema tabular óptimo que deberías exportar desde n8n
datos_largo <- expand.grid(
  Paciente = pacientes_id,
  Codigo = codigos_cif,
  Iteracion = iteraciones_llm
)

# Simulamos la inferencia dicotómica del modelo (0 = Ausente, 1 = Presente)
# Añadimos una ligera ponderación para simular que el LLM asigna ceros a lo que no ve
datos_largo$Prediccion <- sample(
  c(0, 1), 
  size = nrow(datos_largo), 
  replace = TRUE, 
  prob = c(0.7, 0.3) 
)

# =====================================================================
# CÁLCULO 1: ALFA DE KRIPPENDORFF GLOBAL
# =====================================================================

# Para la métrica global, cada "sujeto" es una combinación única de Paciente + Código.
# Tienes 5 pacientes x 15 códigos = 75 sujetos evaluados en 5 repeticiones.
datos_global <- datos_largo %>%
  mutate(Sujeto_Evaluado = paste(Paciente, Codigo, sep = "_")) %>%
  select(Iteracion, Sujeto_Evaluado, Prediccion)

# Pivotamos al formato matricial exigido por la función kripp.alpha
# Regla estricta: Filas = Evaluadores (Iteraciones), Columnas = Sujetos
matriz_global_ancha <- datos_global %>%
  pivot_wider(names_from = Sujeto_Evaluado, values_from = Prediccion)

# Convertimos a formato numérico (eliminando la primera columna de texto de Iteración)
matriz_global <- as.matrix(matriz_global_ancha[, -1])

# Cálculo. El method="nominal" es imperativo porque 0 y 1 son categorías de presencia/ausencia
alfa_global <- kripp.alpha(matriz_global, method = "nominal")

cat("\n--- RESULTADO ALFA GLOBAL ---\n")
print(alfa_global)

# =====================================================================
# CÁLCULO 2: ALFA DE KRIPPENDORFF AISLADO POR CÓDIGO
# =====================================================================

# Analizar los fallos a nivel microscópico es lo que aportará valor al TFM.
# Esta función itera sobre cada código CIF y calcula su estabilidad independiente.
calcular_alfa_codigo <- function(df_codigo) {
  matriz_codigo_ancha <- df_codigo %>%
    select(Iteracion, Paciente, Prediccion) %>%
    pivot_wider(names_from = Paciente, values_from = Prediccion)
  
  matriz <- as.matrix(matriz_codigo_ancha[, -1])
  
  # Utilizamos tryCatch porque kripp.alpha falla matemáticamente si 
  # la matriz no tiene varianza (ej. si el LLM pone '0' a todo en las 5 repeticiones)
  resultado <- tryCatch({
    kripp.alpha(matriz, method = "nominal")$value
  }, error = function(e) NA)
  
  return(resultado)
}

# Ejecutamos el análisis estratificado
resultados_por_codigo <- datos_largo %>%
  group_by(Codigo) %>%
  group_modify(~ data.frame(Alfa_Krippendorff = calcular_alfa_codigo(.x))) %>%
  ungroup() %>%
  arrange(desc(Alfa_Krippendorff))

cat("\n--- RESULTADO ALFA POR CÓDIGO CIF ---\n")
print(resultados_por_codigo)