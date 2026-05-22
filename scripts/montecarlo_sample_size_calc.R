# ==============================================================================
# SCRIPT 1: Simulación de Monte Carlo para Potencia de Kappa de Cohen (TFM)
# ==============================================================================

# Instalar y cargar librería de concordancia si es necesario
if (!require(irr)) install.packages("irr", quiet = TRUE)
library(irr)

# 1. Definición de Parámetros del TFM
n_pacientes <- 80          # Tu muestra real
prevalencia <- 0.50        # Asumimos máxima varianza (el código aparece la mitad de las veces)
kappa_esperado <- 0.80     # Rendimiento que estimamos que tendrá el LLM
kappa_nulo <- 0.60         # Mínimo de utilidad clínica aceptable
iteraciones <- 1000        # Número de "hospitales paralelos" a simular
alpha <- 0.05              # Nivel de significación (5%)

set.seed(42)               # Fijar semilla para que el tribunal pueda replicar el resultado exacto
exitos_estadisticos <- 0   # Contador de cuántas simulaciones logran la significancia

cat("Iniciando simulación de Monte Carlo (", iteraciones, " iteraciones )...\n")

# 2. Bucle de Simulación
for (i in 1:iteraciones) {
  
  # A. Simular diagnósticos del Fisioterapeuta (1 = Síntoma, 0 = No síntoma)
  fisio <- rbinom(n_pacientes, 1, prevalencia)
  
  # B. Calcular probabilidad empírica de acierto del LLM para forzar el kappa esperado
  p_azar <- prevalencia^2 + (1 - prevalencia)^2
  p_acierto_llm <- kappa_esperado * (1 - p_azar) + p_azar
  
  # C. Simular las respuestas del LLM y cruzarlas con el Fisioterapeuta
  acierto <- rbinom(n_pacientes, 1, p_acierto_llm)
  llm <- ifelse(acierto == 1, fisio, 1 - fisio)
  
  # D. Calcular el Kappa de Cohen de esta simulación aislada
  datos <- data.frame(Fisio = fisio, LLM = llm)
  resultado_kappa <- kappa2(datos)
  
  # E. Prueba de hipótesis: ¿Es > 0.60 y estadísticamente significativo?
  SE <- resultado_kappa$value / resultado_kappa$statistic # Extraer error estándar
  z_score_ajustado <- (resultado_kappa$value - kappa_nulo) / SE
  p_valor <- pnorm(z_score_ajustado, lower.tail = FALSE)
  
  # Anotar éxito si pasa los controles clínicos y matemáticos
  if (!is.na(p_valor) && p_valor < alpha && resultado_kappa$value > kappa_nulo) {
    exitos_estadisticos <- exitos_estadisticos + 1
  }
}

# 3. Cálculo e Impresión del Resultado
potencia_final <- (exitos_estadisticos / iteraciones) * 100
cat("====================================================\n")
cat(sprintf("Diseño evaluado: N = %d historias clínicas\n", n_pacientes))
cat(sprintf("Potencia Estadística Lograda: %.1f%%\n", potencia_final))
cat("====================================================\n")