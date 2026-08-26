import json
import subprocess
from pathlib import Path

base_dir = Path('/home/miguelvime/projects/2026-03-11_TFM')
gt_path = base_dir / 'data' / 'physio_created_annotated.json'
f35_path = base_dir / 'results' / 'human_text' / '2026-08-25-flash-3.5-human-annotated.json'

gt_data = json.loads(gt_path.read_text(encoding='utf-8'))
f35_data = json.loads(f35_path.read_text(encoding='utf-8'))

raw_gemma = subprocess.check_output(['git', '-C', str(base_dir), 'show', 'HEAD:results/human_text/human_annotated_gemma.json']).decode('utf-8')
gemma_git = json.loads(raw_gemma)

print(f'GT count: {len(gt_data)}, F35 count: {len(f35_data)}, Gemma git count: {len(gemma_git)}')

for i in range(len(gt_data)):
    gt_id = gt_data[i].get('id_clinical_text', f'{i+1}')
    g_id = gemma_git[i].get('id_clinical_text', f'{i+1}')
    f35_id = f35_data[i].get('id_clinical_text', f'{i+1}')
    print(f'Case {i+1}: GT_id={gt_id}, Gemma_id={g_id}, F35_id={f35_id}')
    print(f'   GT codes:    {sorted(gt_data[i].get("icf_codes", []))}')
    print(f'   Gemma cons:  {sorted(gemma_git[i].get("predicted_icf_codes_consensus", []))}')
    print(f'   F35 cons:    {sorted(f35_data[i].get("predicted_icf_codes_consensus", []))}')
