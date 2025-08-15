from typing import Dict, List
from ..parsers.jd_parser import extract_skills
from ..utils.text import tokenize, dedupe

TIPS = [
    'Use standard headers: Experience, Education, Skills, Projects.',
    'Avoid tables, graphics, or multi-column layouts.',
    'Include measurable impact (numbers, %).',
    'Mirror key phrases from the JD naturally in your bullet points.',
    'Stick to 1–2 pages; use common fonts (Arial/Calibri).'
]

def ats_suggestions(resume_text: str, jd_text: str) -> Dict[str, List[str]]:
    r = set(tokenize(resume_text))
    jd = extract_skills(jd_text)
    missing = [k for k in jd if k not in r]
    return {'missing_keywords': dedupe(missing), 'general_tips': TIPS}
