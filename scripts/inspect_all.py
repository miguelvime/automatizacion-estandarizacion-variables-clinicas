import json
from pathlib import Path

base_dir = Path('/home/miguelvime/projects/2026-03-11_TFM')
llm_dir = base_dir / 'results' / 'llm_text'
human_dir = base_dir / 'results' / 'human_text'

print('=== LLM TEXT ===')
for p in sorted(llm_dir.glob('*.json')):
    d = json.loads(p.read_text(encoding='utf-8'))
    print(f'{p.name}: cases={len(d)}, model={d[0].get("predictor_model")}')

print('\n=== HUMAN TEXT ===')
for p in sorted(human_dir.glob('*.json')):
    try:
        d = json.loads(p.read_text(encoding='utf-8'))
        print(f'{p.name}: cases={len(d)}, model={d[0].get("predictor_model")}')
    except Exception as e:
        print(f'{p.name}: ERROR {e}')
