# Instalar paquete si es necesario
# install.packages("irrCAC")

library(irrCAC)

# =====================================================================
# FUNCIÓN DE SIMULACIÓN MONTE CARLO PARA TAMAÑO MUESTRAL (GWET AC1)
# =====================================================================
calcular_n_simulado <- function(k_iteraciones = 5, 
                                prevalencia_esperada = 0.15, 
                                fiabilidad_esperada = 0.85,
                                margen_error_max = 0.15,
                                simulaciones_por_n = 100) {
  
  # Rango de tamaños de muestra (pacientes) a evaluar: de 15 a 60
  n_candidatos <- seq(15, 60, by = 5)
  resultados_n <- numeric(length(n_candidatos))
  
  cat("Iniciando simulación de Monte Carlo...\n")
  
  for (i in seq_along(n_candidatos)) {
    n <- n_candidatos[i]
    errores_estandar <- numeric(simulaciones_por_n)
    
    for (s in 1:simulaciones_por_n) {
      # 1. Crear matriz N x K
      matriz_sim <- matrix(0, nrow = n, ncol = k_iteraciones)
      
      # 2. Rellenar simulando el comportamiento del LLM
      for (fila in 1:n) {
        # Determinamos si la historia clínica realmente tiene el código (1) o no (0)
        verdad_terreno <- rbinom(1, 1, prevalencia_esperada)
        
        # El LLM acierta según la 'fiabilidad_esperada'
        predicciones <- rbinom(k_iteraciones, 1, fiabilidad_esperada)
        
        # Si la verdad era 0, invertimos las predicciones para simular los verdaderos negativos
        if (verdad_terreno == 0) {
          predicciones <- 1 - predicciones
        }
        matriz_sim[fila, ] <- predicciones
      }
      
      # 3. Calcular AC1 y extraer el error estándar
      # Usamos tryCatch por si alguna matriz generada estocásticamente no tiene varianza
      tryCatch({
        ac1_obj <- gwet.ac1.raw(matriz_sim, weights = "unweighted")
        # El intervalo de confianza al 95% es aprox +/- 1.96 * Error Estándar
        margen_error <- 1.96 * ac1_obj$est$stderr
        errores_estandar[s] <- margen_error
      }, error = function(e) {
        errores_estandar[s] <- NA
      })
    }
    
    # Calculamos el margen de error promedio para este tamaño de N
    margen_medio <- mean(errores_estandar, na.rm = TRUE)
    resultados_n[i] <- margen_medio
    
    cat(sprintf("Evaluando N = %d | Margen de Error Promedio = %.3f\n", n, margen_medio))
    
    # Criterio de parada: Si el margen de error es menor al exigido, encontramos el N óptimo
    if (!is.na(margen_medio) && margen_medio <= margen_error_max) {
      cat("\n>>> TAMAÑO MUESTRAL ÓPTIMO ALCANZADO <<<\n")
      cat(sprintf("Para garantizar un margen de error <= %.2f, necesitas %d pacientes únicas.\n", 
                  margen_error_max, n))
      return(n)
    }
  }
  
  cat("\nNo se alcanzó el margen de error deseado en el rango evaluado. Considera aumentar N máximo.\n")
  return(NA)
}

# Ejecutar la simulación con los parámetros de tu TFM
set.seed(42) # Reproducibilidad
N_optimo <- calcular_n_simulado(k_iteraciones = 5, 
                                prevalencia_esperada = 0.15, # Asumiendo código minoritario
                                fiabilidad_esperada = 0.85,  # Asumiendo buen rendimiento del LLM
                                margen_error_max = 0.15)     # Precisión aceptable del estadístico