import re
from pathlib import Path

scripts_dir = Path('/home/miguelvime/projects/2026-03-11_TFM/scripts/analysis')

for s in sorted(scripts_dir.glob('*.*')):
    text = s.read_text(encoding='utf-8')
    has_old_llm = any(old in text for old in ['2026-08-11', '2026-08-18', 'generator_output.json', 'resumen_f1_score.json'])
    has_old_human = any(old in text for old in ['human_annotated_flash-3.5', 'human_annotated_flash-3.6', 'human_annotated_gemma'])
    has_27 = '27' in text
    
    print(f'{s.name}: old_llm={has_old_llm}, old_human={has_old_human}, has_27={has_27}')
