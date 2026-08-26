import json
import subprocess
from pathlib import Path

base_dir = Path('/home/miguelvime/projects/2026-03-11_TFM')
gt_path = base_dir / 'data' / 'physio_created_annotated.json'
f35_path = base_dir / 'results' / 'human_text' / '2026-08-25-flash-3.5-human-annotated.json'
gemma_target_path = base_dir / 'results' / 'human_text' / '2026-08-26-gemma_human_annotated.json'

gt_data = json.loads(gt_path.read_text(encoding='utf-8'))
raw_gemma = subprocess.check_output(['git', '-C', str(base_dir), 'show', 'HEAD:results/human_text/human_annotated_gemma.json']).decode('utf-8')
gemma_git = json.loads(raw_gemma)

fixed_gemma = []
for i in range(len(gt_data)):
    item_gt = gt_data[i]
    item_g = gemma_git[i]
    
    # Consenso estricto 3/3
    it1 = item_g.get('predicted_icf_it1', [])
    it2 = item_g.get('predicted_icf_it2', [])
    it3 = item_g.get('predicted_icf_it3', [])
    consensus = sorted(list(set(it1) & set(it2) & set(it3)))
    
    entry = {
        'id_code_combination': item_gt.get('id_code_combination'),
        'id_clinical_text': item_gt.get('id_clinical_text'),
        'clinical_text': item_gt.get('clinical_text'),
        'icf_codes': item_gt.get('icf_codes'),
        'predicted_icf_codes_consensus': consensus,
        'predictor_model': 'gemma-4-31b-it',
        'consensus_criteria': 'strict 3/3',
        'predicted_icf_it1': it1,
        'predicted_icf_it2': it2,
        'predicted_icf_it3': it3
    }
    fixed_gemma.append(entry)

gemma_target_path.write_text(json.dumps(fixed_gemma, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Successfully wrote {len(fixed_gemma)} cases to {gemma_target_path}')
