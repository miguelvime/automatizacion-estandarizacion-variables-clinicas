# ==============================================================================
# SCRIPT 2 CORREGIDO: Cálculo de Tamaño Muestral Clásico (Ecuaciones Asintóticas)
# ==============================================================================

# Instalar y cargar la librería matemática estándar para tamaños de muestra Kappa
if (!require(kappaSize)) install.packages("kappaSize", quiet = TRUE)
library(kappaSize)

# 1. Definición de Parámetros Clínicos
kappa_nulo <- 0.60           # Mínimo aceptable
kappa_esperado <- 0.80       # Rendimiento esperado del LLM
# Distribución esperada: 50% No tiene el código CIF, 50% Sí tiene el código CIF
prevalencia <- c(0.50, 0.50) 
potencia_deseada <- 0.80     # Potencia estándar exigida en ensayos (80%)
alpha <- 0.05                # Margen de error Tipo I (5%)

cat("Calculando ecuación asintótica para Kappa de Cohen (Diseño Binario)...\n")

# 2. Ejecución de la Función Correcta
resultado_clasico <- PowerBinary(
  kappa0 = kappa_nulo,
  kappa1 = kappa_esperado,
  props = prevalencia,
  alpha = alpha,
  power = potencia_deseada
)

# 3. Impresión del Resultado
cat("\n====================================================\n")
cat("RESULTADO DE LA FÓRMULA TRADICIONAL:\n")
cat("====================================================\n")
print(resultado_clasico)