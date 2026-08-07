import json
import pandas as pd
import numpy as np

def load_and_transform_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for item in data:
        doc_id = item['id_clinical_text']
        
        # Recopilar todos los códigos únicos evaluados en este documento (Ground Truth + Iteraciones)
        all_codes = set(
            item['icf_codes'] + 
            item['predicted_icf_it1'] + 
            item['predicted_icf_it2'] + 
            item['predicted_icf_it3']
        )
        
        # Crear matriz binaria: 1 si la iteración predijo el código, 0 si no
        for code in all_codes:
            records.append({
                'item_id': f"{doc_id}_{code}",
                'it1': 1 if code in item['predicted_icf_it1'] else 0,
                'it2': 1 if code in item['predicted_icf_it2'] else 0,
                'it3': 1 if code in item['predicted_icf_it3'] else 0
            })
            
    df = pd.DataFrame(records).set_index('item_id')
    return df

def calculate_gwet_ac1(df_ratings):
    """
    Calcula el AC1 de Gwet para datos dicotómicos (0 o 1) con múltiples evaluadores.
    """
    n = len(df_ratings)          # Número total de ítems (doc_code)
    r = len(df_ratings.columns)  # Número de evaluadores (iteraciones del LLM)
    
    # Número de evaluadores que asignaron la categoría '1' y '0' por ítem
    r_i1 = df_ratings.sum(axis=1)
    r_i0 = r - r_i1
    
    # Acuerdo observado (p_a)
    p_a = (1 / n) * ( (r_i1 * (r_i1 - 1) + r_i0 * (r_i0 - 1)) / (r * (r - 1)) ).sum()
    
    # Probabilidad marginal de clasificación (pi_1 y pi_0)
    pi_1 = (1 / n) * (r_i1 / r).sum()
    pi_0 = 1 - pi_1
    
    # Acuerdo esperado por azar (p_e) para clasificación dicotómica
    p_e = 2 * pi_1 * pi_0
    
    # Estadístico AC1
    ac1 = (p_a - p_e) / (1 - p_e)
    
    return ac1, p_a, p_e

# Ejecución
# Reemplaza 'test_codifier_output.json' con la ruta real de tu archivo
df_binary = load_and_transform_data('./data/test_data/test_codifier_output.json')
ac1_score, pa, pe = calculate_gwet_ac1(df_binary)

print(f"Número de ítems evaluados (Documento_Código): {len(df_binary)}")
print(f"Acuerdo Observado (Pa): {pa:.4f}")
print(f"Acuerdo por Azar (Pe):  {pe:.4f}")
print(f"Gwet's AC1:             {ac1_score:.4f}")
