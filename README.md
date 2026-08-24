# Codificación Automatizada de Historias Clínicas a la CIF mediante LLMs y Flujos Orquestados

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![R 4.0+](https://img.shields.io/badge/R-4.0%2B-blue.svg)](https://www.r-project.org/)
[![n8n](https://img.shields.io/badge/orchestrator-n8n-EA4B71.svg)](https://n8n.io/)
[![Docker Compose](https://img.shields.io/badge/docker-compose-2496ED.svg)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pipeline integral para la **extracción, codificación y validación diagnóstica de texto clínico no estructurado a la Clasificación Internacional del Funcionamiento, de la Discapacidad y de la Salud (CIF)** de la OMS mediante LLMs y algoritmos de consenso estricto.

Validado sobre el **Core Set Abreviado de Dolor Crónico Generalizado** (27 códigos CIF).

---

## ⚡ Guía Rápida de Uso (Quickstart)

El repositorio está diseñado tanto para **analizar cualquier base de datos externa** como para **reproducir la memoria científica del TFM**:

```mermaid
flowchart LR
    A[Tus Historias Clínicas en JSON] --> B[1. Codificación en n8n]
    B --> C[Salida JSON Codificada]
    C --> D[2. python analizar_dataset.py]
    D --> E[Dashboard Interactivo HTML + Reporte]
```

### 1. Analizar tu Propia Base de Datos (1 solo paso)
Una vez que hayas codificado tus historias en n8n (o usando cualquier archivo de prueba en `data/test_data/`):

```bash
# Auto-detecta si tienes o no Gold Standard:
python analizar_dataset.py ruta/a/tu_archivo_n8n.json --nombre "Mi Estudio Clínico 2026"
```

* **Si tu archivo contiene etiquetas reales (`icf_codes`):** El sistema calcula métricas de validación ($F_1$-Score, Exact Match, Precisión, Sensibilidad, Matrices de Confusión) y auditoría caso por caso (TP, FP, FN).
* **Si tu archivo solo contiene notas clínicas:** El sistema calcula métricas descriptivas (total de códigos extraídos, ranking de patologías más frecuentes, capítulos CIF afectados y % de acuerdo del consenso 3/3).

---

### 2. Reproducir el Análisis Científico Completo del TFM
Para ejecutar la batería completa de 18 scripts estadísticos, figuras en 300 DPI y tablas Word en formato APA:

```bash
# Opción A: Con Docker (Recomendado - Cero Instalación)
cd infrastructure
docker compose run --rm analysis

# Opción B: En Local (Python + R)
pip install -r requirements.txt
python scripts/analysis/ejecutar_todo.py
```

---

## 🖥️ Dashboard Interactivo y Reporte Ejecutivo

Tras la ejecución, dispones de una interfaz interactiva de archivo único lista para abrir en cualquier navegador con doble clic:
* **Dashboard HTML Autónomo:** [`results/TFL/dashboard_resumen.html`](file:///Ubuntu/home/miguelvime/projects/2026-03-11_TFM/results/TFL/dashboard_resumen.html) *(Scorecards de KPIs, gráficos comparativos interactivos, tabla completa de datos y auditor de historias caso por caso)*.
* **Informe Resumido Markdown:** [`results/TFL/informes/INFORME_EJECUTIVO_METRICAS.md`](file:///Ubuntu/home/miguelvime/projects/2026-03-11_TFM/results/TFL/informes/INFORME_EJECUTIVO_METRICAS.md).

---

## 🚀 Cómo Codificar Historias Clínicas con el LLM en n8n

### 1. Formato del Archivo de Entrada
El flujo en n8n toma como entrada un archivo JSON con historias clínicas (puedes probar directamente con `data/test_data/test_generator_output.json`):

```json
[
  {
    "id_code_combination": "011",
    "id_clinical_text": "011_1",
    "clinical_text": "Varón de 45 años, operario de almacén, acude por dolor generalizado en espalda y extremidades. En tto. con analgésicos pautados sin mejoría. Dificultades para levantar cajas pesadas en el trabajo..."
  }
]
```

### 2. Configurar el LLM y Ejecutar en n8n
1. Levanta n8n con Docker (`cd infrastructure && docker compose up -d n8n`) y ábrelo en `http://localhost:5679`.
2. Importa el flujo `n8n_workflows/2026-08-16_generic_LLM_codifier.json`.
3. Selecciona tu proveedor de LLM:
   * **Google Gemini (Cloud)**: Pega tu API Key gratuita de [Google AI Studio](https://aistudio.google.com/).
   * **Ollama / Gemma (Local On-Premise)**: Si usas Ollama local (`ollama run gemma2:27b`), introduce en la URL `http://host.docker.internal:11434` (si usas Docker) o `http://localhost:11434`.
4. Carga tu archivo JSON y pulsa **Execute Workflow**.

### 3. Salida Generada por n8n
El flujo ejecuta 3 iteraciones independientes y aplica el algoritmo de consenso estricto (`strict 3/3`), produciendo un JSON codificado:

```json
[
  {
    "id_code_combination": "011",
    "id_clinical_text": "011_1",
    "clinical_text": "Varón de 45 años, operario de almacén...",
    "predicted_icf_codes_consensus": [
      "b280",
      "d430",
      "d850",
      "e1101"
    ],
    "consensus_criteria": "strict 3/3",
    "predicted_icf_it1": ["b280", "d430", "d850", "e1101"],
    "predicted_icf_it2": ["b280", "d430", "d850", "e1101"],
    "predicted_icf_it3": ["b280", "d430", "d850", "e1101"]
  }
]
```

---

## 🗂️ Estructura del Repositorio

```
2026-03-11_TFM/
├── analizar_dataset.py           # 🚀 Analizador universal en 1 paso para cualquier archivo JSON
├── infrastructure/               # Docker Compose y Dockerfile (n8n + analysis)
├── data/                         # Datasets de entrada y referencias ontológicas
│   ├── test_data/                # Datos de prueba para probar el flujo inmediatamente
│   ├── generator_input.json      # Combinaciones CIF generadoras
│   ├── physio_created_annotated.json # Gold Standard anotado por 4 fisioterapeutas
│   └── RAG_documents/            # Ontología CIF oficial de la OMS
├── n8n_workflows/                # Flujos de trabajo exportados de n8n
│   ├── 2026-07-28_generator_no_rag.json       # Generador de historias
│   ├── 2026-07-31_codifier_workflow.json      # Codificador base
│   └── 2026-08-16_generic_LLM_codifier.json   # Codificador agnóstico de modelo
├── prompts/                      # Prompts clínicos versionados (codifier y generator)
├── scripts/                      # Código ejecutable
│   ├── codifier/                 # Scripts JS del nodo de consenso en n8n
│   ├── generator/                # Scripts JS del generador en n8n
│   └── analysis/                 # 18 scripts de análisis estadístico + ejecutar_todo.py
└── results/                      # Resultados y artefactos de publicación
    ├── llm_text/                 # Predicciones de los 3 modelos LLM (corpus sintético)
    ├── human_text/               # Predicciones de los 3 modelos LLM (corpus humano)
    └── TFL/                      # Tablas APA (.docx), Figuras 300 DPI, Informes y Dashboard HTML
```

---

## 📊 Scripts de Análisis Estadístico (`scripts/analysis/`)

- `ejecutar_todo.py`: Orquestador maestro que corre toda la batería estadística.
- `01_calculo_confiabilidad_azar.py`: Fiabilidad inter-iteraciones ($\alpha$ de Krippendorff, $AC_1$ de Gwet).
- `03_calculo_f1_score.py`: Validez diagnóstica $F_1$ Micro/Macro con IC 95% Bootstrap.
- `04_calculo_sensibilidad_ablacion.py`: Sensibilidad por ablación de la clase dominante `b280`.
- `06_plot_desempeno.py`: Generación de Figuras 1 a 5 a 300 DPI en `results/TFL/figuras/`.
- `09_generar_tablas_apa.R`: Renderizado de tablas APA en Word (.docx) con `flextable`.
- `13_analisis_human_annotated.py`: Validación sobre historias reales ($N=21$) con Gold Standard de 4 fisioterapeutas.
- `18_generar_dashboard_html.py`: Generador del Dashboard interactivo HTML y reporte ejecutivo Markdown.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
