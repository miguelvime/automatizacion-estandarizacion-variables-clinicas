# Instalar paquetes si no están disponibles:
# install.packages(c("readr", "flextable", "officer", "magrittr"))

library(readr)
library(flextable)
library(officer)
library(magrittr)

# 1. Cargar los datos desde el archivo CSV
# Se asume que el archivo se llama 'resumen_dataset.csv' y está delimitado por punto y coma (;)
# Puedes cambiar la ruta de "resumen_dataset.csv" a la ruta real de tu archivo.
datos <- read_delim("data/results/tablas_publicacion.csv", delim = ";", show_col_types = FALSE)

# 2. Crear y formatear la tabla con estándar de publicación (APA)
tabla_word <- flextable(datos) %>%
  theme_apa() %>% 
  set_caption(caption = "Tabla 1. Estadísticas descriptivas del conjunto de datos clínicos y extracción de códigos ICF.") %>%
  autofit() %>% 
  # Se ajusta la alineación a la columna 2 (Valor) ya que ahora solo hay dos columnas
  align(j = 2, align = "center", part = "all") %>% 
  # Aseguramos que la primera columna esté alineada a la izquierda
  align(j = 1, align = "left", part = "all") %>%
  bold(part = "header")

# 3. Exportar directamente a un documento de Word en tu directorio de trabajo
save_as_docx(
  "Resumen Dataset" = tabla_word, 
  path = "tabla_caracteristicas_dataset.docx"
)