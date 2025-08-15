from typing import Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def relevance_score(resume_text: str, jd_text: str) -> Dict[str, Any]:
    vect = TfidfVectorizer(min_df=1, stop_words='english')
    X = vect.fit_transform([resume_text, jd_text])
    score = float(cosine_similarity(X[0], X[1])[0][0] * 100.0)
    return {'method': 'tfidf', 'score': round(max(0.0, min(100.0, score)), 2)}
