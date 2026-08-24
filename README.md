# Codificación Automatizada de Historias Clínicas a la CIF mediante Modelos de Lenguaje Grande (LLMs) y Flujos Orquestados

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![R 4.0+](https://img.shields.io/badge/R-4.0%2B-blue.svg)](https://www.r-project.org/)
[![n8n](https://img.shields.io/badge/orchestrator-n8n-EA4B71.svg)](https://n8n.io/)
[![Docker Compose](https://img.shields.io/badge/docker-compose-2496ED.svg)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este repositorio contiene el pipeline metodológico, los flujos de orquestación, los datasets de validación y la suite de análisis estadístico desarrollados para la **extracción y codificación automatizada de texto clínico no estructurado a la Clasificación Internacional del Funcionamiento, de la Discapacidad y de la Salud (CIF)** de la Organización Mundial de la Salud (OMS), aplicando Modelos de Lenguaje Grande (LLMs) y estrategias de consenso multi-iteración (*Self-Consistency*).

El sistema está validado sobre el **Core Set Abreviado de la CIF para Dolor Crónico Generalizado / Fibromialgia** (27 categorías ontológicas distribuidas en Funciones Corporales `b`, Actividades y Participación `d` y Factores Ambientales `e`).

---

## ⚡ Inicio Rápido en 1 Minuto

Si acabas de clonar el repositorio, puedes probar todo el proyecto en 3 sencillos pasos:

```bash
# 1. Instalar dependencias de Python
pip install -r requirements.txt

# 2. Ejecutar toda la batería de análisis y generar tablas APA/figuras en 20 segundos
python scripts/analysis/ejecutar_todo.py

# 3. Probar el flujo de codificación en n8n con el dataset de prueba incluido:
# Carga 'n8n_workflows/2026-08-16_generic_LLM_codifier.json' y usa 'data/ejemplo_historias_clinicas.json'
```

---

## 📋 Tabla de Contenidos
- [1. Características Principales](#-1-características-principales)
- [2. Estructura del Repositorio](#-2-estructura-del-repositorio)
- [3. Instalación y Configuración](#-3-instalación-y-configuración)
- [4. Guía de Uso: Cómo Analizar tus Propias Historias Clínicas](#-4-guía-de-uso-cómo-analizar-tus-propias-historias-clínicas)
- [5. Reproducción de Resultados (TFM)](#-5-reproducción-de-resultados-tfm)
- [6. Suite de Scripts de Análisis Estadístico](#-6-suite-de-scripts-de-análisis-estadístico)
- [7. Licencia y Cita](#-7-licencia-y-cita)

---

## 🔬 1. Características Principales

1. **Pipeline Orquestado en n8n**: Automatización modular que procesa historias clínicas en JSON, realiza llamadas paralelas a LLMs, parsea las respuestas estructuradas y aplica algoritmos de consenso.
2. **Estrategia de Auto-Consistencia ($K=3$)**: Ejecución de 3 iteraciones independientes por historia clínica con resolución de consenso estricto (3/3 unánime) o voto mayoritario ($\ge 2/3$) para suprimir alucinaciones.
3. **Evaluación Comparativa Tri-Modelo**:
   - **Gemma-4-31B-it**: Modelo local (*On-Premise*), garantizando la soberanía de los datos clínicos y el cumplimiento estricto del RGPD.
   - **Gemini Flash 3.5**: Modelo en la nube de alta velocidad.
   - **Gemini Flash 3.6**: Modelo en la nube optimizado para razonamiento biomédico.
4. **Doble Validación Metodológica**:
   - **Corpus Sintético *In-Silico*** ($N = 101$ historias clínicas / 114 ejecuciones): Exact Match 98.25%–100%, Micro-$F_1$ 0.969–0.972, Gwet $AC_1$ 0.9994–1.0000.
   - **Corpus Clínico Real Ecológico** ($N = 21$ historias clínicas): Evaluación frente al *Gold Standard* consensuado por **4 fisioterapeutas clínicos independientes** (Micro-$F_1$ 0.822, Precisión 82%–92.5%).
5. **Generación Automática de Tablas y Figuras (TFL)**: Exportación directa de tablas en Word (.docx) con formato editorial **APA / Booktabs** (R `flextable`/`officer`) y figuras a 300 DPI (PNG, SVG, PDF).

---

## 🗂️ 2. Estructura del Repositorio

```
2026-03-11_TFM/
├── infrastructure/               # Infraestructura Docker (compose.yaml)
├── data/                         # Datasets de entrada y referencias
│   ├── ejemplo_historias_clinicas.json # Dataset de prueba listo para usar en n8n
│   ├── generator_input.json      # Combinaciones de códigos CIF generadoras
│   ├── physio_created_annotated.json # Gold Standard anotado por 4 fisioterapeutas
│   └── RAG_documents/            # Ontología CIF oficial de la OMS
├── n8n_workflows/                # Flujos de trabajo exportados de n8n
│   ├── 2026-07-28_generator_no_rag.json       # Generador de historias sintéticas
│   ├── 2026-07-31_codifier_workflow.json      # Codificador base
│   └── 2026-08-16_generic_LLM_codifier.json   # Codificador genérico agnóstico de modelo
├── prompts/                      # Prompts clínicos versionados
│   ├── generator_prompts/        # Prompts de generación
│   └── codifier_prompts/         # Prompts de codificación
├── scripts/                      # Código fuente organizado
│   ├── generator/                # Helpers JS del generador en n8n
│   ├── codifier/                 # Helpers JS del codificador en n8n (consensus, parser, multiplier)
│   └── analysis/                 # 17 scripts estadísticos + ejecutar_todo.py
├── results/                      # Datasets codificados y salidas de publicación
│   ├── llm_text/                 # Corpus sintético (101 casos) y codificaciones LLM
│   ├── human_text/               # Corpus humano (21 casos) y codificaciones LLM
│   └── TFL/                      # Tablas, Figuras y Listados listos para publicación
│       ├── tablas/               # Tablas APA en DOCX, XLSX y CSV
│       ├── figuras/              # Figuras a 300 DPI (PNG, SVG, PDF)
│       ├── listados/             # Listados clínicos de discrepancias
│       └── informes/             # Informes ejecutivos y técnicos (.docx, .md)
├── requirements.txt              # Dependencias de Python
└── README.md                     # Documentación general
```

---

## ⚙️ 3. Instalación y Configuración

### 3.1. Entorno Python
```bash
python3 -m venv .venv
source .venv/bin/activate  # En Linux/WSL (o .venv\Scripts\activate en Windows)
pip install -r requirements.txt
```

### 3.2. Paquetes de R (Opcional - para tablas APA en Word)
```R
install.packages(c("flextable", "officer", "dplyr", "jsonlite", "readr", "magrittr", "tibble"))
```

### 3.3. Despliegue de n8n con Docker
```bash
cd infrastructure
docker compose up -d
```
Acceso a n8n: `http://localhost:5679`

---

## 🚀 4. Guía de Uso: Cómo Analizar tus Propias Historias Clínicas

### Paso 1: Usar el Dataset de Prueba o Cargar el Tuyo
Puedes utilizar directamente el dataset de prueba incluido [data/ejemplo_historias_clinicas.json](file:///Ubuntu/home/miguelvime/projects/2026-03-11_TFM/data/ejemplo_historias_clinicas.json), o crear uno propio con la estructura:

```json
[
  {
    "id_clinical_text": "PACIENTE-001",
    "clinical_text": "Paciente mujer de 48 años con dolor generalizado de más de 6 meses de evolución en zona cervical y lumbar. Refiere rigidez matutina severa, fatiga constante y sueño no reparador. Dificultad para permanecer de pie en su jornada laboral y ayuda familiar en tareas domésticas. En tratamiento con analgésicos pautados."
  }
]
```

### Paso 2: Configurar y Ejecutar en n8n
1. Abre n8n (`http://localhost:5679`).
2. Importa el flujo [n8n_workflows/2026-08-16_generic_LLM_codifier.json](file:///Ubuntu/home/miguelvime/projects/2026-03-11_TFM/n8n_workflows/2026-08-16_generic_LLM_codifier.json).
3. Introduce tu API Key de Gemini o selecciona el endpoint local de Ollama (`http://host.docker.internal:11434`).
4. Selecciona tu archivo JSON de entrada y pulsa **Execute Workflow**.

### Paso 3: Salida Obtenida
El flujo genera un JSON enriquecido con las 3 pasadas y el consenso unánime:
```json
[
  {
    "id_clinical_text": "PACIENTE-001",
    "predicted_icf_it1": ["b134", "b280", "d415", "d640", "e1101", "e310"],
    "predicted_icf_it2": ["b134", "b280", "d415", "d640", "e1101", "e310"],
    "predicted_icf_it3": ["b134", "b280", "d415", "d640", "e1101", "e310"],
    "predicted_icf_codes_consensus": ["b134", "b280", "d415", "d640", "e1101", "e310"]
  }
]
```

---

## 📊 5. Reproducción de Resultados (TFM)

Para reproducir **todos** los análisis estadísticos, matrices de confusión, análisis de sensibilidad por ablación, figuras a 300 DPI y tablas APA en Word del TFM:

### Opción Rápida (1 Comando):
```bash
python scripts/analysis/ejecutar_todo.py
```

### Opción Modular (Paso a Paso):
- **Corpus Sintético ($N=101$)**:
  - Fiabilidad azar: `python scripts/analysis/01_calculo_confiabilidad_azar.py`
  - Exact Match: `python scripts/analysis/02_calculo_acuerdo_exacto.py`
  - Validez $F_1$: `python scripts/analysis/03_calculo_f1_score.py`
  - Ablación $b280$: `python scripts/analysis/04_calculo_sensibilidad_ablacion.py`
  - Figuras: `python scripts/analysis/06_plot_desempeno.py`
  - Tablas APA: `Rscript scripts/analysis/09_generar_tablas_apa.R`
- **Validación Humana ($N=21$)**:
  - Métricas pareadas: `python scripts/analysis/13_analisis_human_annotated.py`
  - Figuras humanas: `python scripts/analysis/14_plot_human_annotated.py`
  - Tablas APA humanas: `Rscript scripts/analysis/15_generar_tablas_human_apa.R`
  - Informe Word: `python scripts/analysis/16_generar_informe_word_completo.py`

---

## 📈 6. Suite de Scripts de Análisis Estadístico

| Script | Lenguaje | Función Principal | Salida en `results/TFL/` |
| :--- | :---: | :--- | :--- |
| `ejecutar_todo.py` | Python/R | **Orquestador maestro**: ejecuta la suite completa y muestra el resumen ejecutivo. | Todas las salidas TFL |
| `01_calculo_confiabilidad_azar.py` | Python | Confiabilidad inter-iteraciones ($\alpha$ de Krippendorff, $AC_1$ de Gwet). | Consola / Métricas |
| `02_calculo_acuerdo_exacto.py` | Python | Acuerdo exacto paciente a paciente y discrepancias. | Auditoría |
| `03_calculo_f1_score.py` | Python | Validez diagnóstica $F_1$ Micro/Macro, IC 95% Bootstrap, 27 códigos CIF. | `tablas/tablas_desempeno.docx` |
| `04_calculo_sensibilidad_ablacion.py` | Python | Análisis de sensibilidad por ablación de la clase dominante `b280`. | `tablas/tabla_sensibilidad_ablacion.csv` |
| `05_generar_tfl_fiabilidad.py` | Python | Generador integral de TFL de fiabilidad y listados. | `tablas/tablas_completas_fiabilidad_word.docx` |
| `06_plot_desempeno.py` | Python | Figuras 1 a 5 de desempeño diagnóstico tri-modelo. | `figuras/01_` a `05_` (PNG 300 DPI) |
| `07_plot_eficiencia_f1.py` | Python | Gráfico de compensación coste computacional vs $F_1$. | `figuras/06_eficiencia_estrategias_consenso_f1.png` |
| `08_plot_sensibilidad_ablacion.py` | Python | Gráfico de retención tras ablación de $b280$. | `figuras/06_ablacion_b280_comparativa_modelos.png` |
| `09_generar_tablas_apa.R` | R | Tablas APA de desempeño diagnóstico con `flextable`. | `tablas/tablas_desempeno.docx` |
| `10_generar_tabla_fiabilidad_apa.R` | R | Tabla APA de fiabilidad inter-iteraciones en Word. | `tablas/tabla_fiabilidad_apa.docx` |
| `11_generar_tabla_consenso_apa.R` | R | Tabla APA de estrategias de consenso ($K=1$ vs $K=3$). | `tablas/tabla_estrategias_consenso_apa.docx` |
| `12_tabla_sensibilidad_ablacion_apa.R` | R | Tabla APA de ablación de la clase `b280`. | `tablas/tabla_sensibilidad_ablacion_apa.docx` |
| `13_analisis_human_annotated.py` | Python | Evaluación frente al Gold Standard de 4 fisioterapeutas. | `human_text/resumen_human_annotated.json` |
| `14_plot_human_annotated.py` | Python | Figuras de validación humana y benchmarking real vs sintético. | `figuras/01_` a `05_` humanas (PNG 300 DPI) |
| `15_generar_tablas_human_apa.R` | R | Tablas APA de validación humana en Word. | `tablas/tablas_validacion_humana_apa.docx` |
| `16_generar_informe_word_completo.py` | Python | Informe clínico ejecutivo de validación humana en Word. | `informes/informe_validacion_historias_humanas.docx` |
| `17_workflow_diagram.py` | Python | Diagrama metodológico completo del pipeline (PNG, SVG, PDF). | `figuras/workflow_linear_es.*` |

---

## 📄 7. Licencia y Cita

Este proyecto está bajo la Licencia MIT. Para citar este trabajo:

```bibtex
@mastersthesis{vime2026tfm,
  author       = {Miguel Vime},
  title        = {Codificación automatizada de historias clínicas a la Clasificación Internacional del Funcionamiento (CIF) mediante Modelos de Lenguaje Grande (LLMs) y flujos orquestados},
  school       = {Universidad / Programa de Máster en Salud Digital e IA Clínica},
  year         = {2026},
  month        = {Agosto},
  type         = {Trabajo de Fin de Máster (TFM)}
}
```
