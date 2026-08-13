
from sklearn.feature_extraction.text import TfidfVectorizer


def fit_vectorizer(corpus):
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus)
    return vectorizer, matrix