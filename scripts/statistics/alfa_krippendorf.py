import json
import numpy as np
import krippendorff

def load_and_transform_for_krippendorff(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 1. Identificar todos los pares únicos (documento_código)
    items = []
    for item in data:
        doc_id = item['id_clinical_text']
        all_codes = set(
            item['icf_codes'] + 
            item['predicted_icf_it1'] + 
            item['predicted_icf_it2'] + 
            item['predicted_icf_it3']
        )
        for code in all_codes:
            items.append((doc_id, code))
            
    # 2. Crear matriz: filas = iteraciones (evaluadores), columnas = ítems (doc_code)
    # 3 iteraciones equivalen a 3 filas
    matrix = np.zeros((3, len(items)))
    
    for col_idx, (doc_id, code) in enumerate(items):
        # Buscar el documento original en el JSON
        doc_data = next(d for d in data if d['id_clinical_text'] == doc_id)
        
        # Asignar 1 si la iteración predijo el código, 0 en caso contrario
        matrix[0, col_idx] = 1 if code in doc_data['predicted_icf_it1'] else 0
        matrix[1, col_idx] = 1 if code in doc_data['predicted_icf_it2'] else 0
        matrix[2, col_idx] = 1 if code in doc_data['predicted_icf_it3'] else 0
        
    return matrix, items

# Ejecución (Asegúrate de ejecutar: pip install krippendorff)
matrix, item_labels = load_and_transform_for_krippendorff('./data/test_data/test_codifier_output.json')

# Calcular el Alfa de Krippendorff para datos nominales (ausencia/presencia de código)
alpha = krippendorff.alpha(reliability_data=matrix, level_of_measurement='nominal')

print(f"Evaluadores (Iteraciones): {matrix.shape[0]}")
print(f"Ítems evaluados (Pares Doc-Código): {matrix.shape[1]}")
print(f"Krippendorff's Alpha: {alpha:.4f}")
