# Informe de Tablas, Figuras y Listados (TFL): Fiabilidad Inter-Iteraciones (Sección 6.6.1 / 7.1)

Este informe contiene los resultados cuantitativos definitivos, tablas formateadas para publicación médica y gráficos vectoriales/alta resolución correspondientes a la **Sección 6.6.1 (Metodología)** y **Sección 7.1 (Resultados)** del TFM.

## 1. Tabla 1: Confiabilidad y Reproducibilidad Inter-Iteraciones (K = 3)

| Modelo LLM Evaluado | Tipo de Despliegue | Historias | Exact Match (3/3) | Acuerdo Po (%) | Gwet's AC1 | Krippendorff α |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Gemma-4-31B-it** | Local (On-Premise) | 114 | 107/114 (93.86%) | 99.8294% | 0.9976 | 0.9940 |
| **Gemini Flash 3.5 (Cloud - Línea Base)** | Cloud (API) | 114 | 102/114 (89.47%) | 99.6589% | 0.9952 | 0.9882 |
| **Gemini Flash 3.7** | Cloud (API) | 114 | 108/114 (94.74%) | 99.8538% | 0.9980 | 0.9948 |

> **Interpretación metodológica:** Un valor de $\alpha > 0.80$ y $AC1 > 0.80$ denota acuerdo casi perfecto (Landis & Koch / Krippendorff). Tanto el despliegue local (Gemma) como en la nube (Gemini Flash) demuestran determinismo operativo virtualmente perfecto ($>0.998$).

## 2. Tabla 2: Desglose del Espacio de Decisiones Binarias (2.736 Unidades Ontológicas)

| Modelo LLM | Unidades Totales | Asignación Unánime SÍ [1,1,1] | Abstención Unánime NO [0,0,0] | Discrepancias (<3/3) | Determinismo Paciente |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gemma-4-31B-it** | 2736 | 470 (17.18%) | 2259 (82.57%) | 7 (0.26%) | 107/114 (93.86%) |
| **Gemini Flash 3.5 (Cloud - Línea Base)** | 2736 | 472 (17.25%) | 2250 (82.24%) | 14 (0.51%) | 102/114 (89.47%) |
| **Gemini Flash 3.7** | 2736 | 465 (17.00%) | 2265 (82.79%) | 6 (0.22%) | 108/114 (94.74%) |


## 3. Listado 1: Auditoría de Historias Clínicas con Discrepancias

| Modelo | Historia | Iteración 1 | Iteración 2 | Iteración 3 | Consenso (3/3) | Código Discrepante |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| Gemma-4-31B-it | #14 | b280, d230, d430, d450, d640 | b280, d230, d430, d450, d640 | b147, b280, d230, d430, d450, d640 | b280, d230, d430, d450, d640 | `b147` |
| Gemma-4-31B-it | #34 | b280, e410 | b280, e410 | b280, e310, e410 | b280, e410 | `e310` |
| Gemma-4-31B-it | #59 | b130, d240, d920, e410 | b130, b152, d240, d920, e410 | b130, d240, d920, e410 | b130, d240, d920, e410 | `b152` |
| Gemma-4-31B-it | #61 | b134, b280, e1101, e410 | b134, b280, e1101, e310, e410 | b134, b280, e1101, e410 | b134, b280, e1101, e410 | `e310` |
| Gemma-4-31B-it | #102 | b147, b152, b280, b760, d450 | b147, b280, b760, d450 | b147, b152, b280, b760, d450 | b147, b280, b760, d450 | `b152` |
| Gemma-4-31B-it | #104 | b280, b730, b760, d450, d850 | b280, b730, d450, d850 | b280, b730, d450, d850 | b280, b730, d450, d850 | `b760` |
| Gemma-4-31B-it | #111 | b130, b280, b455, d450, e1101, e355 | b130, b280, b455, d230, d450, e1101, e355 | b130, b280, b455, d230, d450, e1101, e355 | b130, b280, b455, d450, e1101, e355 | `d230` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #5 | b152, b1602, b280, d240, d850, e570 | b130, b152, b1602, b280, d240, d850, e570 | b130, b152, b1602, b280, d240, d850, e570 | b152, b1602, b280, d240, d850, e570 | `b130` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #7 | b134, b152, b280, d240, d640, d760, d920, e310, e410 | b134, b152, b280, d240, d640, d760, d920, e410 | b134, b152, b280, d240, d640, d760, d920, e310, e410 | b134, b152, b280, d240, d640, d760, d920, e410 | `e310` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #9 | b134, b152, b280, d240, d640, d760, d920, e410 | b134, b152, b280, d240, d640, d760, d920, e310, e410 | b134, b152, b280, d240, d640, d760, d920, e310, e410 | b134, b152, b280, d240, d640, d760, d920, e410 | `e310` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #51 | b130, b147, b280 | b130, b147, b280 | b130, b147, b280, b455 | b130, b147, b280 | `b455` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #58 | b130, d230, d240, d770, d920, e410 | b130, d230, d240, d770, d920, e310, e410 | b130, d230, d240, d920, e410 | b130, d230, d240, d920, e410 | `d770, e310` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #63 | b134, b280, d760, e1101, e310, e410 | b134, b280, d760, e1101, e410 | b134, b280, d760, e1101, e310, e410 | b134, b280, d760, e1101, e410 | `e310` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #73 | b147, b280, b730, b760, d770, e410 | b147, b280, b730, b760, e410 | b147, b280, b730, b760, d770, e410 | b147, b280, b730, b760, e410 | `d770` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #75 | b147, b280, b730, b760, e410 | b147, b280, b730, b760, d760, e410 | b147, b280, b730, b760, d760, e310, e410 | b147, b280, b730, b760, e410 | `d760, e310` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #81 | b1602, b280, d770, e1101, e355 | b1602, b280, d770, e1101, e355 | b152, b1602, b280, d770, e1101, e355 | b1602, b280, d770, e1101, e355 | `b152` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #88 | b280, d175, d920, e310, e410 | b280, d175, d920, e410 | b280, d175, d920, e410 | b280, d175, d920, e410 | `e310` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #90 | b152, b280, d175, d920, e310, e410 | b152, b280, d175, d920, e410 | b152, b280, d175, d920, e310, e410 | b152, b280, d175, d920, e410 | `e310` |
| Gemini Flash 3.5 (Cloud - Línea Base) | #105 | b280, b730, d450, d850 | b280, b730, b760, d450, d850 | b280, b730, d450, d850 | b280, b730, d450, d850 | `b760` |
| Gemini Flash 3.7 | #7 | b134, b152, b280, d240, d640, d760, d920, e410 | b134, b152, b280, d240, d640, d760, d920, e310, e410 | b134, b152, b280, d240, d640, d760, d920, e310, e410 | b134, b152, b280, d240, d640, d760, d920, e410 | `e310` |
| Gemini Flash 3.7 | #9 | b134, b152, b280, d240, d640, d760, d920, e410 | b134, b152, b280, d240, d640, d760, d920, e310, e410 | b134, b152, b280, d240, d640, d760, d920, e410 | b134, b152, b280, d240, d640, d760, d920, e410 | `e310` |
| Gemini Flash 3.7 | #34 | b280, e410 | b280, d770, e410 | b280, d770, e410 | b280, e410 | `d770` |
| Gemini Flash 3.7 | #62 | b134, b280, e1101, e355, e410 | b134, b280, e1101, e355, e410 | b134, b280, e1101, e310, e355, e410 | b134, b280, e1101, e355, e410 | `e310` |
| Gemini Flash 3.7 | #63 | b134, b280, d760, e1101, e410 | b134, b280, d760, e1101, e410 | b134, b280, e1101, e410 | b134, b280, e1101, e410 | `d760` |
| Gemini Flash 3.7 | #102 | b147, b280, b760, d450 | b147, b152, b280, b760, d450 | b147, b280, b760, d450 | b147, b280, b760, d450 | `b152` |


## 4. Figuras Generadas para Publicación

- **Figura 1**: `results/stats_v4/TFL/figuras/figura1_comparativa_fiabilidad_modelos.png` (PNG 300 DPI, SVG, PDF)
- **Figura 2**: `results/stats_v4/TFL/figuras/figura2_espacio_decisiones_binarias.png` (PNG 300 DPI, SVG, PDF)

