# Informe de Tablas, Figuras y Listados (TFL): Fiabilidad Inter-Iteraciones (Sección 6.6.1 / 7.1)

Este informe contiene los resultados cuantitativos definitivos, tablas formateadas para publicación médica y gráficos vectoriales/alta resolución correspondientes a la **Sección 6.6.1 (Metodología)** y **Sección 7.1 (Resultados)** del TFM.

## 1. Tabla 1: Confiabilidad y Reproducibilidad Inter-Iteraciones (K = 3)

| Modelo LLM Evaluado | Tipo de Despliegue | Historias | Exact Match (3/3) | Acuerdo Po (%) | Gwet's AC1 | Krippendorff α |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Gemma-4-31B-it (Local)** | Local (On-Premise) | 114 | 112/114 (98.25%) | 99.9567% | 0.9994 | 0.9983 |
| **Gemini Flash 3.5 (Cloud - Línea Base)** | Cloud (API) | 114 | 112/114 (98.25%) | 99.9567% | 0.9994 | 0.9983 |
| **Gemini Flash 3.6 (Cloud)** | Cloud (API) | 114 | 114/114 (100.00%) | 100.0000% | 1.0000 | 1.0000 |

> **Interpretación metodológica:** Un valor de $\alpha > 0.80$ y $AC1 > 0.80$ denota acuerdo casi perfecto (Landis & Koch / Krippendorff). Tanto el despliegue local (Gemma) como en la nube (Gemini Flash) demuestran determinismo operativo virtualmente perfecto ($>0.998$).

## 2. Tabla 2: Desglose del Espacio de Decisiones Binarias (3.078 Unidades Ontológicas)

| Modelo LLM | Unidades Totales | Asignación Unánime SÍ [1,1,1] | Abstención Unánime NO [0,0,0] | Discrepancias (<3/3) | Determinismo Paciente |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gemma-4-31B-it (Local)** | 3078 | 464 (15.07%) | 2612 (84.86%) | 2 (0.06%) | 112/114 (98.25%) |
| **Gemini Flash 3.5 (Cloud - Línea Base)** | 3078 | 463 (15.04%) | 2613 (84.89%) | 2 (0.06%) | 112/114 (98.25%) |
| **Gemini Flash 3.6 (Cloud)** | 3078 | 462 (15.01%) | 2616 (84.99%) | 0 (0.00%) | 114/114 (100.00%) |


## 3. Listado 1: Auditoría de Historias Clínicas con Discrepancias

| Modelo | Historia | Iteración 1 | Iteración 2 | Iteración 3 | Consenso (3/3) | Código Discrepante |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| Gemma-4-31B-it (Local) | #45 | b280, d850, e1101, e355, e570 | b280, d850, e1101, e355 | b280, d850, e1101, e355 | b280, d850, e1101, e355 | `e570` |
| Gemma-4-31B-it (Local) | #62 | b134, b280, e1101, e310, e410 | b134, b280, e1101, e310, e410 | b134, b280, e1101, e310, e355, e410 | b134, b280, e1101, e310, e410 | `e355` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #19 | b134, b280, e1101 | b134, b280, e1101, e355 | b134, b280, e1101 | b134, b280, e1101 | `e355` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #62 | b134, b280, e1101, e310, e355, e410 | b134, b280, e1101, e310, e410 | b134, b280, e1101, e310, e355, e410 | b134, b280, e1101, e310, e410 | `e355` |
| Gemini Flash 3.6 (Cloud) | Todas (114/114) | - | - | - | 100% Determinista | Ninguno (0) |


## 4. Figuras Generadas para Publicación

- **Figura 1**: `results/stats_v4/TFL/figuras/figura1_comparativa_fiabilidad_modelos.png` (PNG 300 DPI, SVG, PDF)
- **Figura 2**: `results/stats_v4/TFL/figuras/figura2_espacio_decisiones_binarias.png` (PNG 300 DPI, SVG, PDF)

