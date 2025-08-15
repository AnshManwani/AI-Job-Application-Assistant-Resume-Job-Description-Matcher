import os
from typing import List, Dict
import pandas as pd
from datetime import datetime

CSV_PATH = os.getenv('CSV_PATH', 'applications.csv')
COLUMNS = ['timestamp','company','role','job_link','match_score','status','next_followup','notes']

def _ensure_file():
    if not os.path.exists(CSV_PATH):
        pd.DataFrame(columns=COLUMNS).to_csv(CSV_PATH, index=False)

def add_application(company: str, role: str, job_link: str, match_score: float, status: str, next_followup: str, notes: str = ''):
    _ensure_file()
    row = {
        'timestamp': datetime.utcnow().isoformat(timespec='seconds') + 'Z',
        'company': company, 'role': role, 'job_link': job_link,
        'match_score': match_score, 'status': status,
        'next_followup': next_followup, 'notes': notes
    }
    df = pd.read_csv(CSV_PATH)
    df = pd.concat([pd.DataFrame([row]), df], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)

def list_applications() -> pd.DataFrame:
    _ensure_file()
    return pd.read_csv(CSV_PATH)
