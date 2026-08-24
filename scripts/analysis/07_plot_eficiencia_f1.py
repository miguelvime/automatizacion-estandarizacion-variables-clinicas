# -*- coding: utf-8 -*-
"""
Plot de comparación de F1-Scores agrupado por Modelo LLM
Permite evaluar intra-modelo el impacto de las 4 estrategias de inferencia (K=1 vs K=3)
Resolución: 300 DPI | Estilo Publicación Médica
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
CARPETA_FIGURAS = BASE_DIR / "results" / "TFL" / "figuras"
CARPETA_FIGURAS.mkdir(parents=True, exist_ok=True)

# Modelos (Eje X principal)
modelos = ["Gemma-4-31B-it", "Gemini Flash 3.5", "Gemini Flash 3.6"]

# 4 Estrategias de inferencia
estrategias = [
    "Pase Único (K=1, Coste 1x)",
    "Consenso Estricto (3/3, Coste 3x)",
    "Voto Mayoritario (≥ 2/3, Coste 3x)",
    "Unión / Sensibilidad (≥ 1/3, Coste 3x)"
]

# Valores de Micro-F1 por modelo para cada una de las 4 estrategias
# Filas: 4 estrategias | Columnas: 3 modelos
datos_f1 = np.array([
    [0.9699, 0.9709, 0.9709],  # Pase Único (K=1)
    [0.9688, 0.9720, 0.9709],  # Consenso Estricto (3/3)
    [0.9688, 0.9709, 0.9709],  # Voto Mayoritario (≥ 2/3)
    [0.9689, 0.9699, 0.9709]   # Unión (≥ 1/3)
])

# Paleta armónica para las 4 estrategias
colores_estrategias = [
    "#1F4E79",  # Azul oscuro elegante (Pase Único 1x)
    "#2E86C1",  # Azul medio (Consenso Estricto 3/3 3x)
    "#5DADE2",  # Azul claro (Voto Mayoritario ≥ 2/3 3x)
    "#F39C12"   # Ámbar suave (Unión ≥ 1/3 3x)
]

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10.5
plt.rcParams['xtick.labelsize'] = 10.5
plt.rcParams['ytick.labelsize'] = 9.5
plt.rcParams['legend.fontsize'] = 9.0
plt.rcParams['figure.dpi'] = 300

fig, ax = plt.subplots(figsize=(10.5, 5.5))

x = np.arange(len(modelos))
ancho_barra = 0.18
offsets = [-1.5 * ancho_barra, -0.5 * ancho_barra, 0.5 * ancho_barra, 1.5 * ancho_barra]

for i in range(len(estrategias)):
    vals = datos_f1[i]
    barras = ax.bar(
        x + offsets[i],
        vals,
        width=ancho_barra,
        label=estrategias[i],
        color=colores_estrategias[i],
        alpha=0.90,
        edgecolor="black",
        linewidth=0.7
    )
    
    # Etiquetas numéricas sobre las barras
    for bar in barras:
        y_pos = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            y_pos + 0.0006,
            f"{y_pos:.4f}",
            ha='center',
            va='bottom',
            fontsize=8.0,
            fontweight='bold',
            rotation=90
        )

ax.set_ylabel("Micro-F1 Score", fontweight='bold')
# ax.set_title("Comparativa Intra-Modelo de la Eficacia Diagnóstica (Micro-F1) según la Estrategia de Consenso", fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(modelos, fontweight='bold', fontsize=11)
ax.set_ylim(0.955, 0.985)
ax.grid(axis='y', linestyle=':', alpha=0.6)

# Leyenda profesional
ax.legend(
    frameon=True,
    facecolor='#F8F9F9',
    edgecolor='#BDC3C7',
    loc="lower right"
)

plt.tight_layout()
ruta_salida = CARPETA_FIGURAS / "06_eficiencia_estrategias_consenso_f1.png"
plt.savefig(ruta_salida, dpi=300)
plt.close()
print(f" [OK] Plot agrupado por modelo guardado en: {ruta_salida}")
