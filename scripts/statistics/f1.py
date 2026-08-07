import json
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

def evaluate_clinical_coding(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    y_true = []
    y_pred_consensus = []
    
    for item in data:
        # Ground Truth
        y_true.append(item['icf_codes'])
        # Predicción a evaluar (usamos el consenso, pero podrías iterar por it1, it2, etc.)
        y_pred_consensus.append(item['predicted_icf_codes_consensus'])
    
    # Binarizar las listas de códigos multietiqueta
    mlb = MultiLabelBinarizer()
    
    # Ajustar el binarizador con todos los códigos posibles (reales + predichos)
    all_codes = y_true + y_pred_consensus
    mlb.fit(all_codes)
    
    # Transformar a matrices binarias
    y_true_bin = mlb.transform(y_true)
    y_pred_bin = mlb.transform(y_pred_consensus)
    
    # --- CÁLCULO DE MÉTRICAS ---
    
    # 1. Exact Match Ratio (EMR)
    # accuracy_score en scikit-learn con matrices multietiqueta calcula el EMR exacto
    emr = accuracy_score(y_true_bin, y_pred_bin)
    
    # 2. Micro Métricas (Agrega las contribuciones de todas las clases para calcular la métrica)
    micro_precision = precision_score(y_true_bin, y_pred_bin, average='micro', zero_division=0)
    micro_recall = recall_score(y_true_bin, y_pred_bin, average='micro', zero_division=0)
    micro_f1 = f1_score(y_true_bin, y_pred_bin, average='micro', zero_division=0)
    
    # 3. Macro Métricas (Calcula las métricas para cada etiqueta y encuentra su media no ponderada)
    macro_precision = precision_score(y_true_bin, y_pred_bin, average='macro', zero_division=0)
    macro_recall = recall_score(y_true_bin, y_pred_bin, average='macro', zero_division=0)
    macro_f1 = f1_score(y_true_bin, y_pred_bin, average='macro', zero_division=0)

    # 4. Métricas Ponderadas (Weighted - Ajusta por el desbalanceo real de las clases)
    weighted_precision = precision_score(y_true_bin, y_pred_bin, average='weighted', zero_division=0)
    weighted_recall = recall_score(y_true_bin, y_pred_bin, average='weighted', zero_division=0)
    weighted_f1 = f1_score(y_true_bin, y_pred_bin, average='weighted', zero_division=0)

    # Imprimir resultados
    print(f"Total de textos clínicos evaluados: {len(y_true)}")
    print("-" * 40)
    print(f"Exact Match Ratio (EMR): {emr:.4f}")
    print("-" * 40)
    print("MÉTRICAS MICRO (Global, maneja desbalanceo):")
    print(f"  Micro Precision: {micro_precision:.4f}")
    print(f"  Micro Recall:    {micro_recall:.4f}")
    print(f"  Micro F1-Score:  {micro_f1:.4f}")
    print("-" * 40)
    print("MÉTRICAS MACRO (Penaliza fallos en clases minoritarias):")
    print(f"  Macro Precision: {macro_precision:.4f}")
    print(f"  Macro Recall:    {macro_recall:.4f}")
    print(f"  Macro F1-Score:  {macro_f1:.4f}")
    print("-" * 40)
    print("MÉTRICAS WEIGHTED (Ponderadas por soporte real):")
    print(f"  Weighted Precision: {weighted_precision:.4f}")
    print(f"  Weighted Recall:    {weighted_recall:.4f}")
    print(f"  Weighted F1-Score:  {weighted_f1:.4f}")

# Ejecución
evaluate_clinical_coding('./data/test_data/test_codifier_output.json')
