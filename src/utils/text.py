import re
import nltk

# Ensure resources (download on first run)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))

def normalize(text: str) -> str:
    text = (text or '').replace('\x00', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text: str):
    text = (text or '').lower()
    tokens = re.findall(r'[a-zA-Z][a-zA-Z0-9\-\+\#\.]*', text)
    return [t for t in tokens if t not in STOPWORDS]

def dedupe(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out
