import json
import os
from collections import Counter
import matplotlib
import numpy as np
import pandas as pd
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =====================================================================
# 1. CARGA DE DATOS REALES
# =====================================================================
file_path = './data/results/generator_output.json'

print("Iniciando procesamiento de la base de datos...")
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(f"Total de registros clínicos cargados: {len(data)}")
except FileNotFoundError:
    print(f"Error crítico: No se encontró el archivo en {file_path}.")
    exit(1)
except json.JSONDecodeError:
    print("Error crítico: El archivo JSON está corrupto o mal formateado.")
    exit(1)

# =====================================================================
# 2. EXTRACCIÓN Y CÁLCULO DE MÉTRICAS
# =====================================================================
code_counter = Counter()
codes_per_record = []

for entry in data:
    codes = entry.get("icf_codes", [])
    if isinstance(codes, list):
        code_counter.update(codes)
        codes_per_record.append(len(codes))
    else:
        codes_per_record.append(0)

total_unique_codes = len(code_counter)
total_extracted_codes = sum(code_counter.values())
total_records = len(data)

if total_records == 0 or total_extracted_codes == 0:
    print("Error: El archivo JSON está vacío o no contiene códigos ICF.")
    exit(1)

mean_codes = np.mean(codes_per_record) if codes_per_record else 0
std_codes = np.std(codes_per_record) if codes_per_record else 0
median_codes = np.median(codes_per_record) if codes_per_record else 0

print(f"Códigos ICF únicos identificados: {total_unique_codes}")
print(f"Frecuencia absoluta (total de códigos extraídos): {total_extracted_codes}")

# =====================================================================
# 3. CÁLCULO DE FRECUENCIAS RELATIVAS (Sumatorio = 100%)
# =====================================================================
all_codes = []
relative_frequencies = []

for code, count in code_counter.most_common():
    all_codes.append(code)
    # CÁLCULO ACTUALIZADO: (Frecuencia del código / Total de códigos extraídos) * 100
    rel_freq = (count / total_extracted_codes) * 100
    relative_frequencies.append(rel_freq)

print(f"Suma de todas las proporciones calculadas: {sum(relative_frequencies):.2f}%")

# =====================================================================
# 4. VISUALIZACIÓN GRÁFICA
# =====================================================================
os.makedirs('./data/results', exist_ok=True)
top_n = min(50, total_unique_codes)

plt.figure(figsize=(16, 6))
bars = plt.bar(all_codes[:top_n], relative_frequencies[:top_n], color='#4C72B0', edgecolor='black')

plt.title(f'Frecuencia Relativa Top {top_n} Códigos ICF\n(Total de Códigos extraídos = {total_extracted_codes}, Códigos Únicos = {total_unique_codes})')
plt.xlabel('Código ICF')
plt.ylabel('Frecuencia Relativa (%)')

max_freq = max(relative_frequencies[:top_n]) if relative_frequencies else 100
plt.ylim(0, max_freq * 1.25) 
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=90) 

font_size = 8 if top_n > 20 else 10
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + (max_freq * 0.02), 
             f'{yval:.1f}%', ha='center', va='bottom', fontsize=font_size, rotation=90)

plt.tight_layout()
output_png = './data/results/frecuencia_relativa_codigos.png'
plt.savefig(output_png, dpi=300, bbox_inches='tight')
print(f"Gráfico exportado con éxito a: {output_png}")

# =====================================================================
# 5. GENERACIÓN DE TABLAS PARA PUBLICACIÓN
# =====================================================================
summary_data = {
    "Variable": [
        "Registros clínicos evaluados (N)",
        "Total de códigos ICF extraídos (n)",
        "Códigos ICF únicos identificados (n)",
        "Códigos por historia clínica (Media ± DE)",
        "Códigos por historia clínica (Mediana)"
    ],
    "Valor": [
        total_records,
        total_extracted_codes,
        total_unique_codes,
        f"{mean_codes:.2f} ± {std_codes:.2f}",
        f"{median_codes:.1f}"
    ]
}
df_summary = pd.DataFrame(summary_data)

table_codes_data = {
    "Código ICF": all_codes,
    "Frecuencia absoluta (n)": [count for _, count in code_counter.most_common()],
    "Frecuencia relativa (%)": [round((count / total_extracted_codes) * 100, 2) for _, count in code_counter.most_common()]
}
df_codes = pd.DataFrame(table_codes_data)

excel_output_path = './data/results/tablas_publicacion.xlsx'
try:
    with pd.ExcelWriter(excel_output_path, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name='Resumen_Dataset', index=False)
        df_codes.to_excel(writer, sheet_name='Frec_Relativa_Codigos', index=False)
    print(f"Tablas exportadas con éxito a: {excel_output_path}")
except Exception as e:
    print(f"Aviso: Error con openpyxl ({e}). Exportando a CSV...")
    csv_output_path = './data/results/frec_relativa_codigos.csv'
    df_codes.to_csv(csv_output_path, sep=';', index=False, encoding='utf-8-sig')
    print(f"Exportado a: {csv_output_path}")