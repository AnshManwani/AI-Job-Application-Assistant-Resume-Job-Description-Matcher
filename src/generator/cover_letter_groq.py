import os
from typing import Dict
from groq import Groq

SYSTEM_PROMPT = (
    "You are a concise, professional cover-letter writer. "
    "Write a one-page letter with: 1) a strong opening, 2) two short skill-impact bullets, "
    "3) a closing call-to-action. Mirror relevant keywords naturally for ATS. "
    "Tone: confident, specific, no fluff."
)

def generate_cover_letter_groq(resume_text: str, jd_text: str, applicant_name: str, company: str, role: str, model: str = None) -> Dict:
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise RuntimeError('Missing GROQ_API_KEY in environment')
    client = Groq(api_key=api_key)
    model = model or os.getenv('GROQ_MODEL', 'llama3-8b-8192')

    user_prompt = f"""Company: {company or 'N/A'}
Role: {role or 'N/A'}

Job Description:
{jd_text}

Resume:
{resume_text}

Write the letter addressed to the hiring manager. Sign with: {applicant_name}.
"""

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_prompt},
        ],
        temperature=0.6,
        max_tokens=650,
    )
    content = resp.choices[0].message.content
    return {'cover_letter': content}
