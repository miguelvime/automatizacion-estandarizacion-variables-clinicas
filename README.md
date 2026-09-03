# Codificación Automatizada de Historias Clínicas a la CIF mediante LLMs

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![R 4.0+](https://img.shields.io/badge/R-4.0%2B-blue.svg)](https://www.r-project.org/)
[![n8n](https://img.shields.io/badge/orchestrator-n8n-EA4B71.svg)](https://n8n.io/)
[![Docker Compose](https://img.shields.io/badge/docker-compose-2496ED.svg)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pipeline integral para la **extracción, codificación y validación diagnóstica de texto clínico no estructurado a la Clasificación Internacional del Funcionamiento (CIF)** de la OMS mediante LLMs y consenso estricto (3/3). Validado sobre 24 categorías CIF de Dolor Crónico.

---

## ⚡ Reproducir el Estudio en 1 Minuto

Para ejecutar toda la batería de análisis (métricas $F_1$, confiabilidad inter-iteraciones, figuras 300 DPI y tablas APA en Word):

### Opción A: Con Docker (Recomendado — 1 solo comando)
```bash
cd infrastructure && docker compose run --rm analysis
```

### Opción B: En Local (Python + R)
```bash
# 1. Instalar dependencias
pip install -r requirements.txt
Rscript -e "install.packages(c('flextable', 'officer', 'dplyr', 'jsonlite', 'readr', 'magrittr', 'tibble'), repos='https://cloud.r-project.org')"

# 2. Ejecutar la batería completa
python scripts/analysis/ejecutar_todo.py
```

### 📊 ¿Dónde ver los resultados?
Tras la ejecución, abre directamente en tu navegador o explorador:
* **Dashboard Interactivo:** Doble clic en [`results/TFL/dashboard_resumen.html`](results/TFL/dashboard_resumen.html).
* **Tablas Word en formato APA:** En la carpeta `results/TFL/tablas/`.
* **Figuras en 300 DPI (PNG / PDF):** En la carpeta `results/TFL/figuras/`.
* **Informe Resumen Ejecutivo:** [`results/TFL/informes/INFORME_EJECUTIVO_METRICAS.md`](results/TFL/informes/INFORME_EJECUTIVO_METRICAS.md).

---

## 🔍 Analizar tu Propia Base de Datos (1 solo paso)

Para evaluar cualquier archivo JSON codificado (o probar el flujo con datos de test):

```bash
python analizar_dataset.py data/test_data/test_codifier_output.json --nombre "Mi Estudio Clínico"
```
*Detecta automáticamente si el archivo tiene Gold Standard (calculando $F_1$, precisión, recall y matrices de confusión) o si son notas clínicas sin etiquetar (calculando prevalencias y frecuencias).*

---

## 🤖 Codificación con LLMs en n8n

Para reproducir la codificación con los modelos desde cero:

1. **Levantar n8n:** `cd infrastructure && docker compose up -d n8n` (accede en `http://localhost:5679`).
2. **Importar el flujo:** Importa desde `n8n_workflows/` el flujo del modelo que quieras evaluar:
   * `2026-08-25-gemini-3.7-flash-codifier.json` (Gemini Flash 3.7)
   * `2026-08-25-gemini-3.5-flash-codifier.json` (Gemini Flash 3.5)
   * `2026-08-25-gemma-4-31b-it-codifier.json` (Gemma-4-31B-it vía Ollama local)
3. **Credenciales:** Pega tu API Key de Gemini o apunta a tu instancia de Ollama (`http://localhost:11434`).
4. **Ejecutar:** Carga las historias clínicas (`data/generator_output.json`) y pulsa **Execute Workflow**.

---

## 🗂️ Estructura del Repositorio

```
2026-03-11_TFM/
├── scripts/analysis/ejecutar_todo.py  # 🚀 Orquestador maestro que corre toda la batería estadística
├── analizar_dataset.py               # Analizador universal para cualquier JSON
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
