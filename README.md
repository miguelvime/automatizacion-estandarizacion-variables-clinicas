# Codificación Automatizada de Historias Clínicas a la CIF mediante LLMs

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![R 4.0+](https://img.shields.io/badge/R-4.0%2B-blue.svg)](https://www.r-project.org/)
[![n8n](https://img.shields.io/badge/orchestrator-n8n-EA4B71.svg)](https://n8n.io/)
[![Docker Compose](https://img.shields.io/badge/docker-compose-2496ED.svg)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pipeline integral para la **extracción, codificación y validación diagnóstica de texto clínico no estructurado a la Clasificación Internacional del Funcionamiento (CIF)** de la OMS mediante LLMs y algoritmos de consenso estricto (3/3). Validado sobre 24 categorías CIF de Dolor Crónico.

---

## ⚡ 1. Reproducir el Estudio del TFM en 1 Minuto

Para regenerar toda la batería estadística (métricas $F_1$, confiabilidad, figuras a 300 DPI y tablas Word APA):

### Opción A: Con Docker (Recomendado — 1 solo comando)
```bash
cd infrastructure && docker compose run --rm analysis
```

### Opción B: En Local (Python + R)
```bash
# 1. Instalar dependencias
pip install -r requirements.txt
Rscript -e "install.packages(c('flextable', 'officer', 'dplyr', 'jsonlite', 'readr', 'magrittr', 'tibble'), repos='https://cloud.r-project.org')"

# 2. Ejecutar
python scripts/analysis/ejecutar_todo.py
```

> **📊 ¿Dónde ver los resultados?**  
> Abre en tu navegador [`results/TFL/dashboard_resumen.html`](results/TFL/dashboard_resumen.html) para explorar las métricas interactivas, o consulta las carpetas `results/TFL/tablas/` (Word APA) y `results/TFL/figuras/` (300 DPI).

---

## 🌐 2. Usar la Herramienta con tu Propia Base de Datos

El sistema es **universal y modular**: puedes usarlo para codificar y analizar tus propias historias clínicas hospitalarias en solo 2 pasos:

### Paso 1: Codificar tus textos clínicos
Prepara un archivo JSON con tus notas clínicas (solo requiere el campo `clinical_text`):
```json
[
  { "id_clinical_text": "01", "clinical_text": "Paciente de 45 años con dolor lumbar crónico y limitación funcional..." }
]
```
Impórtalo en el flujo de **n8n** (ver sección abajo) para procesarlo con tu LLM preferido. Obtendrás un JSON codificado con consenso estricto 3/3.

### Paso 2: Generar Dashboard y Reporte (1 solo comando)
```bash
python analizar_dataset.py ruta/a/tu_archivo_codificado.json --nombre "Mi Hospital / Cohorte 2026"
```
* **Auto-detección inteligente:**
  * **Si incluye Gold Standard (`icf_codes`):** Calcula métricas diagnósticas completas ($F_1$-Score, Exact Match, Precisión, Sensibilidad y matrices de confusión caso a caso).
  * **Si solo incluye texto clínico:** Genera métricas descriptivas poblacionales (prevalencia de patologías, categorías CIF más frecuentes y porcentaje de acuerdo).
* **Salida instantánea:** Genera automáticamente un **Dashboard HTML interactivo autónomo** en `results/TFL/dashboard_resumen.html` y un informe ejecutivo en `results/TFL/informes/INFORME_EJECUTIVO_METRICAS.md`.

---

## 🤖 3. Configurar y Ejecutar n8n

1. **Levantar el servicio:** `cd infrastructure && docker compose up -d n8n` (accede en `http://localhost:5679`).
2. **Importar el flujo:** En la interfaz de n8n, importa desde `n8n_workflows/` el flujo del modelo deseado:
   * `2026-08-25-gemini-3.7-flash-codifier.json` (Google Gemini 3.7 Flash)
   * `2026-08-25-gemini-3.5-flash-codifier.json` (Google Gemini 3.5 Flash)
   * `2026-08-25-gemma-4-31b-it-codifier.json` (Gemma-4-31B-it)
   * `2026-09-03_generic_LLM_codifier.json` es un workflow genérico que puedes adaptar a cualquier modelo.
3. **Ejecutar:** pulsa **Execute Workflow**, se abrirá una ventana para cargar tu archivo JSON a codificar.

---

## 🗂️ Estructura del Repositorio

```
2026-03-11_TFM/
├── scripts/analysis/ejecutar_todo.py  # 🚀 Orquestador maestro que reproduce el TFM
├── analizar_dataset.py               # 🔍 Analizador universal de 1 paso para cualquier dataset
├── data/                             # Datasets (generator_output.json [N=114], physio_created [N=21])
├── n8n_workflows/                    # Flujos de orquestación de n8n para Gemini y Gemma
├── infrastructure/                   # Docker Compose y Dockerfile listos para usar
├── results/                          # Salidas generadas:
│   └── TFL/                          # Dashboard HTML, Figuras 300 DPI y Tablas Word APA
└── requirements.txt                  # Dependencias de Python
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
