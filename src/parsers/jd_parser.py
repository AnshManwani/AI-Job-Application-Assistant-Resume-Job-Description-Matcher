from typing import List
from pathlib import Path
from ..utils.text import tokenize, dedupe

SKILLS_PATH = Path(__file__).resolve().parents[2] / 'data' / 'skills.txt'

def _load_skill_dict() -> List[str]:
    if SKILLS_PATH.exists():
        return [s.strip().lower() for s in SKILLS_PATH.read_text(encoding='utf-8').splitlines()
                if s.strip() and not s.strip().startswith('#')]
    return ['python','sql','docker','aws','pandas','numpy']

DICT = set(_load_skill_dict())

def extract_skills(text: str) -> List[str]:
    tok = tokenize(text)
    skills = [t for t in tok if t in DICT]
    return dedupe(skills)
